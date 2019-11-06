from asyncio import Task, new_event_loop, as_completed, ensure_future
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, cpu_count
from scapy.all import wrpcap
from time import strftime
from queue import Empty
import signal
import sys

class TestLogger(Process):
	"""Class for logging tests results"""

	_instance = None
	
	def __new__(cls, *args, **kwargs):
		if TestLogger._instance is None:
			TestLogger._instance = object.__new__(cls)
		return TestLogger._instance

	def __init__(self, log_dir, log_queue):
		super().__init__()
		self.log_queue = log_queue                                           # FIFO queue for logging from other instances
		self._result_directory_name = log_dir + "/" + "MegacoTester_Results_" + strftime("%d.%m.%Y_%Hh-%Mm-%Ss")  # Name of the results logging directory
		self._event_loop = new_event_loop()                                  # Getting an event loop for asynchronous task processing
		self._thread_executor = ThreadPoolExecutor(max_workers=cpu_count())  # Thread pool for blocking tasks (number of workers = number of CPUs)
		self._stop_counter = 0                                               # Counts the stop frames (when it is equal 2, it stops the event loop)
		self._parse_logs = {"success" : [], "failure" : []}                  # Collects tests files parsing results
		self._create_result_directory()                                      # Creates a results logging directory with subdirectories

	def signal_handler(self):
		"""Signal handler for asynchronous event loop

		Stops it gracefully and dumps the tests files parsing log
		"""
		with open("/dev/null") as sys.stderr:
			self._thread_executor.shutdown(wait=False)
			[task.cancel() for task in Task.all_tasks() if task is not Task.current_task()]
			self._event_loop.stop()
			self._dump_test_parser_log()

	def _create_result_directory(self):
		"""Creates a results logging directory with subdirectories"""
		FileSystem.create_dir(self._result_directory_name)
		FileSystem.create_dir(self._result_directory_name + "/" + "Log")
		FileSystem.create_dir(self._result_directory_name + "/" + "Dump")

	def _form_test_parser_log(self):
		"""Forms the tests parsing log in single string for further writing to Test_Parser.log"""
		test_parser_log = "SUCCESSFULLY PARSED:\n"
		for parse_log in self._parse_logs["success"]:
			test_parser_log += parse_log
		test_parser_log += "\nUNSUCCESSFULLY PAPSED:\n"
		for parse_log in self._parse_logs["failure"]:
			test_parser_log += parse_log
		return test_parser_log

	def _dump_test_parser_log(self):
		"""Writes the formed parsing log string to Test_Parser.log"""
		FileSystem.dump_to(self._result_directory_name + "/" + "Test_Parser.log", self._form_test_parser_log())

	@staticmethod
	def _write_test_dump(pcap_file, dump):
		"""Writes all catched packets to the test pcap-file"""
		for packet in dump:
			wrpcap(pcap_file, packet, append=True)

	async def _record_logs(self, report):
		"""Handles the frame payload in the thread executor"""
		if report.action == Frame.Report.PARSE:
			# Collects the tests parsing log for further writing to Test_Parser.log
			if report.success:
				self._parse_logs["success"] += [report.log]
			else:
				self._parse_logs["failure"] += [report.log]
		elif report.action == Frame.Report.EXECUTE:
			# Writes a test log and dump to the results directory
			test_log = ("EXECUTE STATUS: SUCCESS\n\n" if report.success else "EXECUTE STATUS: FAILURE\n\n") + report.log
			for task in as_completed([self._event_loop.run_in_executor(self._thread_executor, FileSystem.dump_to, 
				                                                       self._result_directory_name + "/Log/" + report.test_name + ".log", test_log)]):
				await task
			for task in as_completed([self._event_loop.run_in_executor(self._thread_executor, TestLogger._write_test_dump, 
				                                                       self._result_directory_name + "/Dump/" + report.test_name + ".pcap", report.dump)]):
				await task

	async def _main_coro(self):
		"""Creates tasks for asynchronous event loop"""
		while True:
			try:
				# Gets a frame from the log queue in a separate thread
				for task in as_completed([self._event_loop.run_in_executor(self._thread_executor, self.log_queue.get, True, 0.1)]):
					frame = await task
					# If the current frame is a STOP frame, increase the counter.
					# Handles the frame payload otherwise
					if frame.header == Frame.STOP:
						self._stop_counter += 1
					else:
						await self._record_logs(frame.payload)
			except Empty:
				# Event loop works while TestParser and Processor generate tasks
				if self._stop_counter == 2:
					break

	def run(self):
		# Add SIGINT and SIGTERM trap for event loop
		for signame in ("SIGINT", "SIGTERM"):
			self._event_loop.add_signal_handler(getattr(signal, signame), lambda: ensure_future(self.signal_handler()))
		# Running the asynchronous event loop
		self._event_loop.run_until_complete(self._main_coro())
		# Stop the asynchronous event loop
		self._event_loop.close()
		# Dumps the tests files parsing log
		self._dump_test_parser_log()