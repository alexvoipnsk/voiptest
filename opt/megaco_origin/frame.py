class Frame:
	"""Class that defines the composition of messages exchanged between application components

	The Frame instance has two fields: header (mandatory) and payload (optional)
	The Frame instance can have one of two payload types - Test, Report - or None
	"""

	STOP, TEST, REPORT = range(3)  # Defines the types of Frame headers

	def __init__(self, header, payload=None):
		self.header = header
		self.payload = payload

	class Test:
		"""Class that defines the Test payload of Frame

		The Test instance has two mandatory fields: name and instructions
		"""
		
		def __init__(self, name, instructions):
			self.name = name
			self.instructions = instructions

	class Report:
		"""Class that defines the Report payload of Frame"""

		PARSE, EXECUTE = range(2)  # Defines the types of reported actions
		
		def __init__(self, action, success, log, dump=None, test_name=None):
			self.action = action        # Reported action (PARSE or EXECUTE)
			self.success = success      # Success indicator (True or False)
			self.test_name = test_name  # Reported test name
			self.log = log              # Reported test log
			self.dump = dump            # Reported test dump