from random import randint
from time import strftime

class Megaco:
	"""Class for implementing of Megaco protocol"""

	def __init__(self):
		self._generators = self._define_generators()  # Protocol value generators

	def _define_generators(self):
		"""Defines and returns the protocol value generators"""
		return {
		    "transaction_id" : Megaco._generate_uint32,
		    "context_id" : Megaco._generate_uint32,
		    "request_id" : Megaco._generate_uint32,
		    "timestamp" : Megaco._generate_timestamp
		}

	@staticmethod
	def _generate_uint32():
		"""Returns a random uint32 value"""
		return str(randint(1, 4294967295))

	@staticmethod
	def _generate_timestamp():
		"""Returns a timestamp per ISO 8601"""
		return strftime("%Y%m%dT%H%M%S")

	def generate_value(self, variable):
		"""Generates and returns the requested value of a variable or None"""
		if variable in self._generators:
			return self._generators[variable]()