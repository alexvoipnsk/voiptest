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

	def parse_arguments(self):
		"""Parses command-line arguments

		Returns config file path and list of tests files paths
		"""
		namespace = self._parser.parse_args()
		return (namespace.config, namespace.tests)