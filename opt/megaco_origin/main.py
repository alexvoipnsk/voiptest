#!/usr/bin/env python3
import sys
if sys.version_info < (3,6):
	print("\033[1;31mInterpreter Error:\033[1;m use Python interpreter version 3.6 or greater")
	sys.exit(1)

from os import geteuid

# Check root privileges
if geteuid() != 0:
	print("\033[1;31mPermission Error:\033[1;m you need root privileges")
	exit(1)

# Importing class for working with file system
from file_system import FileSystem

# Importing classes for parsing purposes
from parser.arg_parser import ArgParser
from parser.config_parser import ConfigParser
from parser.test_parser import TestParser

# Importing class for tests processing
from processor.core import Processor

# Importing classes for logging purposes
from test_logger import TestLogger
from application_logger import AppLogger

# Importing classes for main instances interaction
from frame import Frame
from multiprocessing import Queue

# Importing functions and attributes for UNUX signal handling
from signal import signal, SIGINT

# Make FileSystem, AppLogger and Frame classes available in all modules
setattr(__builtins__, 'FileSystem', FileSystem)
setattr(__builtins__, 'AppLogger', AppLogger)
setattr(__builtins__, 'Frame', Frame)

def main():

	def signal_handler(*args):
		with open("/dev/null") as sys.stderr:
			for process in (test_parser, processor, test_logger):
				if process.is_alive():
					process.terminate()
					process.join()
		AppLogger.warning("The application was immediately stopped")
		sys.exit(1)

	# Add SIGINT trap
	signal(SIGINT, signal_handler)

	# Parsing the command-line arguments
	config_file, tests_files = ArgParser().parse_arguments()

	AppLogger.info("Сommand-line arguments was fetched")

	# Parsing the configuration file
	config = ConfigParser().parse_config(config_file)

	# Creating two synchronization queues between program threads
	queues = [Queue() for i in range(2)]

	# Creating and configuring a parser for test scenarios
	AppLogger.info("Creating the TestParser instance ...")
	test_parser = TestParser(tests_files, test_queue=queues[0], log_queue=queues[1])
	AppLogger.info("The TestParser instance was created [OK]")

	# Creating and configuring the processor
	AppLogger.info("Creating the Processor instance ...")
	processor = Processor(config, test_queue=queues[0], log_queue=queues[1])
	AppLogger.info("The Processor instance was created [OK]")

	# Creating and configuring a logger for test scenarios
	AppLogger.info("Creating the TestLogger instance ...")
	test_logger = TestLogger(log_dir=config.log_dir, log_queue=queues[1])
	AppLogger.info("The TestLogger instance was created [OK]")

	# Launching the main instances of application
	AppLogger.info("Running application processes ...")
	test_logger.start()
	processor.start()
	test_parser.start()
	AppLogger.info("Application processes is running [OK]")

	# Stopping the main instances of application
	test_parser.join()
	processor.join()
	test_logger.join()
	AppLogger.info("The application is complete")

if __name__ == "__main__":
	main()