from random import randint
from time import strftime

class Sip:
	"""Class for implementing of Sip protocol"""

	def __init__(self):
		self._generators = self._define_generators()  # Protocol value generators

	def _define_generators(self):
		"""Defines and returns the protocol value generators"""
		return {
		    "branch" : Sip._generate_branch, 
		    "tag" : Sip._generate_tag, 
		    "call_id" : Sip._generate_callid,
		    "return" : Sip._make_return,
		    "timestamp" : Sip._generate_timestamp
		}

	@staticmethod
	def _generate_branch():
		"""Returns a random uint32 value"""
		return "z9hG4bK" + str(randint(1, 4294967295))

	@staticmethod
	def _generate_tag():
		"""Returns a random uint32 value"""
		return "sptstr" + str(randint(1, 4294967295))

	def _generate_callid():
		"""Returns a random uint32 value"""
		return "sptstr-" + str(randint(1, 4294967295)) + "-" + str(randint(1, 4294967295))

	@staticmethod
	def _generate_uint32():
		"""Returns a random uint32 value"""
		return str(randint(1, 4294967295))

	@staticmethod
	def _make_return():
		"""Returns 0d0a"""
		return "\r\n"

	@staticmethod
	def _generate_timestamp():
		"""Returns a timestamp per ISO 8601"""
		return strftime("%Y%m%dT%H%M%S")

	def generate_value(self, variable):
		"""Generates and returns the requested value of a variable or None"""
		if variable in self._generators:
			return self._generators[variable]()