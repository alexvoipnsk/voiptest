from argparse import ArgumentParser

class ArgParser:
	"""Class for command-line arguments parsing"""

	_instance = None

	def __new__(cls, *args, **kwargs):
		if ArgParser._instance is None:
			ArgParser._instance = object.__new__(cls)
		return ArgParser._instance

	def __init__(self):
		self._parser = ArgumentParser()  # Creating a private argparser instanse
		self._define_args()              # Configuring the argparser instance

	def _define_args(self):
		"""Defines command-line arguments and configures argparser"""
		self._parser.add_argument("-c", "--config", action="store", type=str, dest="config", required=True)
		self._parser.add_argument("-t", "--tests", action="store", nargs="+", type=str, dest="tests", required=True)
		self._parser.add_argument("-l", "--logging", action="store_true", required=False, dest="logging", help="set logging usage")
		self._parser.add_argument("-v", "--verbose", action="count", required=False, dest="verbose", help="set verbose level, use -v (CRITICAL), -vv (ERROR), -vvv (WARNING), -vvvv (INFO), -vvvvv (DEBUG)")
		self._parser.add_argument("-j", "--job", action="store", required=False, dest="job", help="set job name")

	def parse_arguments(self):
		"""Parses command-line arguments

		Returns config file path and list of tests files paths
		"""
		namespace = self._parser.parse_args()
		return (namespace.config, namespace.tests, namespace.logging, namespace.verbose, namespace.job)