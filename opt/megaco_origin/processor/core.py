from processor.interpreter import ScenarioInterpreter
from processor.scenario_builder import ScenarioBuilder
from threading import Thread, Event
from multiprocessing import Process
from scapy.all import sniff
from queue import Empty
from time import sleep
import lxml.etree as xml
import sys

class Processor(Process):
	"""Class for executing tests scenarios"""

	_instance = None
	_builder = None
	_sniffer = None
	_interpreter = None

	def __new__(cls, *args, **kwargs):
		if Processor._instance is None:
			Processor._instance = object.__new__(cls)
		return Processor._instance

	def terminate(self):
		"""Terminates the Processor process gracefully

		Stops sniffing and closes all network sockets before termination
		"""
		AppLogger.warning("Stop tests execution")
		with open("/dev/null") as sys.stderr:
			Processor._sniffer.stop(no_wait=True)
			Processor._interpreter.stop_all_network_adapters()
			super().terminate()

	def __init__(self, config, test_queue, log_queue):
		super().__init__()
		self.test_queue = test_queue            # FIFO queue from the TestParser instance 
		self.log_queue = log_queue              # FIFO queue to the TestLogger instance
		Processor._builder = ScenarioBuilder()  # Builder for the Scenario instance
		Processor._sniffer = Sniffer()          # Sniffer for collecting a test dump
		Processor._interpreter = ScenarioInterpreter(config)  # Interpreter for Scenario instances

	def _execute_test(self, test):
		"""Builds and executes the Scenario instance"""
		scenario = Processor._builder.build_scenario(xml.fromstring(test.instructions))
		AppLogger.info("\033[95mStart the test execution:\033[0m '%s'" % test.name)
		# Start sniffing
		Processor._sniffer.start(test.name)
		# Start scenario execution
		result, log = Processor._interpreter.execute(scenario)
		# Stop sniffing
		Processor._sniffer.stop()
		AppLogger.info("%s is " % test.name + ("successfully" if result else "unsuccessfully") + " completed")
		# Gets all packets from sniffer buffer and sends scenario logs to TestLogger
		self.log_queue.put(Frame(Frame.REPORT, Frame.Report(Frame.Report.EXECUTE, result, log, Processor._sniffer.get_buffer(), test.name)))

	def run(self):
		"""Gets and executes test scenarios from TestParser queue"""
		while True:
			try:
				# Fetch frame from TestParser queue
				frame = self.test_queue.get(block=True, timeout=0.1)
				# Stops Processor when frame type is Stop
				# Else exucutes the test scenario
				if frame.header == Frame.STOP:
					break
				else:
					self._execute_test(frame.payload)
			except Empty:
				continue
		# Closes all network sockets before finishes
		Processor._interpreter.stop_all_network_adapters()
		# Send stop frame at the end of execution of tests scenarios
		self.log_queue.put(Frame(Frame.STOP))

class Sniffer:
	"""Class for collecting the test dump"""
	
	def __init__(self):
		self._sniff_thread = None   # Sniffing thread
		self._packet_buffer = None  # Buffer for collected packets
		self._pcap_filename = None  # Name for pcap file
		self._event = Event()       # Event for graceful stop the sniffing thread

	def _dump_packet(self, packet):
		"""Dumps the single packet to buffer"""
		self._packet_buffer.append(packet)

	def _reset_all(self):
		"""Resets all sniffer settings for new sniffing thread"""
		self._sniff_thread = None
		self._packet_buffer = []
		self._event.clear()

	def start(self, pcap_filename):
		"""Starts sniffing thread and collects received packets to buffer"""
		self._reset_all()
		self._pcap_filename = pcap_filename
		# Create and start sniffer thread with event for graceful stop
		self._sniff_thread = Thread(target=sniff, kwargs={"prn" : self._dump_packet, "stop_filter" : lambda p: self._event.isSet(), "store" : 0})
		self._sniff_thread.start()
		# Timeout for sniffer initiating
		sleep(1)

	def get_buffer(self):
		"""Returns the buffer with collected packets"""
		return self._packet_buffer

	def stop(self, no_wait=False):
		"""Stops the sniffer thread by event"""
		if not no_wait:
			# Timeout for catching all received packets 
			sleep(1)        
		self._event.set()
		if self._sniff_thread is not None:
			self._sniff_thread.join()