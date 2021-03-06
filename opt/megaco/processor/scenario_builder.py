class ScenarioBuilder:
	"""Class for building the Scenario instance from validated contents of the test file"""

	_instance = None

	def __new__(cls, *args, **kwargs):
		if ScenarioBuilder._instance is None:
			ScenarioBuilder._instance = object.__new__(cls)
		return ScenarioBuilder._instance

	def __init__(self):
		self._scenario = None                 # Scenario instance
		self._makers = self._define_makers()  # Makers for building the Scenario instructions

	def _define_makers(self):
		return {"define" : self._make_define,
		        "connect" : self._make_connect,
		        "disconnect" : self._make_disconnect,
		        "send" : self._make_send,
		        "recv" : self._make_recv,
		        "actions" : self._make_actions,
		        "catch" : self._make_catch,
		        "compare" : self._make_compare,
		        "assign" : self._make_assign,
		        "print" : self._make_print,
		        "exit" : self._make_exit,
		        "nop" : self._make_nop,
		        "pause" : self._make_pause,
		        "validate" : self._make_validate,
		        "authenticate" : self._make_authenticate,
		        "getbytes" : self._make_getbytes}

	def _make_define(self, component):
		"""Builds the Define instruction of the Scenario instance

		Adds created Define instruction to Scenario instructions
		"""
		self._scenario.instructions.append(Scenario.Define(component.attrib))

	def _make_connect(self, component):
		"""Builds the Connect instruction of the Scenario instance

		Adds created Connect instruction to Scenario instructions
		"""
		self._scenario.instructions.append(Scenario.Connect(int(component.attrib["connection"]), str(component.attrib["mode"])))

	def _make_disconnect(self, component):
		"""Builds the Disconnect instruction of the Scenario instance

		Adds created Disconnect instruction to Scenario instructions
		"""
		self._scenario.instructions.append(Scenario.Disconnect(int(component.attrib["connection"])))

	def _make_send(self, component):
		"""Builds the Send instruction of the Scenario instance

		Adds created Send instruction to Scenario instructions
		"""
		send = Scenario.Send(int(component.attrib["connection"]), component.text.strip())
		if "protocol" in component.attrib:
			send.protocol = str(component.attrib["protocol"])
		else:
			send.protocol = "none"
		if "stream" in component.attrib:
			send.stream = int(component.attrib["stream"])
		self._scenario.instructions.append(send)

	def _make_recv(self, component):
		"""Builds the Recv instruction of the Scenario instance

		Adds created Recv instruction to Scenario instructions
		"""
		if "timeout" in component.attrib:
			recv = Scenario.Recv(int(component.attrib["connection"]), int(component.attrib["timeout"]))
		else:
			recv = Scenario.Recv(int(component.attrib["connection"]))
		if "sec_connection" in component.attrib:
			recv.sec_connection = int(component.attrib["sec_connection"])
		# Building an Actions instruction
		recv.instructions = self._make_actions(component.getchildren()[0]) if component.getchildren() else []
		# Adding the created Recv instruction to Scenario instructions
		self._scenario.instructions.append(recv)

	def _make_actions(self, component):
		"""Builds and returns the Actions instruction of the Scenario instance"""
		actions = Scenario.Actions()
		actions.instructions = [self._makers[instruction.tag](instruction) for instruction in component if instruction.tag in self._makers]
		return actions

	def _make_validate(self, component):
		"""Builds the Validate instruction of the Scenario instance

		Adds created Validate instruction to Scenario instructions
		"""
		if "num" in component.attrib:
			return Scenario.Validate(str(component.attrib["rule"]), component.text.strip(), int(component.attrib["num"]))
		else:
			return Scenario.Validate(str(component.attrib["rule"]), component.text.strip())

	def _make_authenticate(self, component):
		"""Builds and returns the Authenticate instruction of the Scenario instance"""
		return Scenario.Authenticate(component.attrib["assign_to"], component.text.strip())

	def _make_catch(self, component):
		"""Builds and returns the Catch instruction of the Scenario instance"""
		catch = Scenario.Catch(component.attrib["regexp"], component.attrib["assign_to"])
		if "match" in component.attrib:
			catch.match = int(component.attrib["match"])
		return catch

	def _make_getbytes(self, component):
		"""Builds and returns the GetBytes instruction of the Scenario instance"""
		getbytes = Scenario.GetBytes(component.attrib["frombyte"], component.attrib["assign_to"])
		if "tobyte" in component.attrib:
			getbytes.tobyte = int(component.attrib["tobyte"])
		return getbytes

	def _make_compare(self, component):
		"""Builds and returns the Compare instruction of the Scenario instance"""
		compare = Scenario.Compare(component.attrib["first"], component.attrib["second"])
		compare.instructions = [self._makers[instruction.tag](instruction) for instruction in component if instruction.tag in self._makers]
		return compare

	def _make_assign(self, component):
		"""Builds and returns the Assign instruction of the	Scenario instance"""
		return Scenario.Assign(component.attrib["values"], component.attrib["to"])

	def _make_print(self, component):
		"""Builds and returns the Print instruction of the Scenario instance"""
		return Scenario.Print(component.attrib["text"])

	def _make_exit(self, component):
		"""Builds and returns the Exit instruction of the Scenario instance"""
		exit = Scenario.Exit(component.attrib["status"])
		if "info" in component.attrib:
			exit.info = component.attrib["info"]
		return exit

	def _make_nop(self, component):
		"""Builds the Nop instruction of the Scenario instance

		Adds created Nop instruction to Scenario instructions
		"""
		nop = Scenario.Nop()
		nop.instructions = self._make_actions(component.getchildren()[0]) if component.getchildren() else []
		self._scenario.instructions.append(nop)

	def _make_pause(self, component):
		"""Builds and returns the Pause instruction of the Scenario instance"""
		return Scenario.Pause(int(component.attrib["timeout"]))
	
	def build_scenario(self, content):
		"""Builds and returns the Scenario instance"""
		self._scenario = Scenario()                     # Creating a new Scenario instance
		for component in content:
			if component.tag in self._makers:           # Ignore xml comments
				self._makers[component.tag](component)  # Building the Scenario instructions
		return self._scenario

class Scenario:

	def __init__(self):
		self.instructions = []
		self._current_index = 0

	def __iter__(self):
		return self

	def __next__(self):
		if self._current_index >= len(self.instructions):
			raise StopIteration
		else:
			self._current_index += 1
			return self.instructions[self._current_index - 1]

	class Define:
		
		def __init__(self, variables):
			self.variables = variables

	class Connect:
		
		def __init__(self, connection, mode):
			self.connection = connection
			self.mode = mode

	class Disconnect:
		
		def __init__(self, connection):
			self.connection = connection
		
	class Send:
		
		def __init__(self, connection, message, stream = 0):
			self.connection = connection
			self.message = message
			self.stream = stream

	class Recv:

		def __init__(self, connection, timeout=5000, sec_connection=99999):
			self.connection = connection
			self.timeout = timeout
			self.sec_connection = sec_connection
			self.instructions = None

	class Actions:

		def __init__(self):
			self.instructions = None
			self._current_index = 0

		def __iter__(self):
			return self

		def __next__(self):
			if self._current_index >= len(self.instructions):
				raise StopIteration
			else:
				self._current_index += 1
			return self.instructions[self._current_index - 1]

	class Catch:

		def __init__(self, regexp, assign_to):
			self.regexp = regexp
			self.match = 0
			self.assign_to = assign_to

	class GetBytes:

		def __init__(self, frombyte, assign_to):
			self.frombyte = frombyte
			self.tobyte = None
			self.assign_to = assign_to

	class Compare:

		def __init__(self, first, second):
			self.first = first
			self.second = second
			self.instructions = None

	class Assign:

		def __init__(self, values, to):
			self.values = values
			self.to = to

	class Print:

		def __init__(self, text):
			self.text = text

	class Exit:

		def __init__(self, status):
			self.status = status
			self.info = None

	class Nop:

		def __init__(self):
			self.instructions = None
			self._current_index = 0

		def __iter__(self):
			return self

		def __next__(self):
			if self._current_index >= len(self.instructions):
				raise StopIteration
			else:
				self._current_index += 1
			return self.instructions[self._current_index - 1]

	class Pause:

		def __init__(self, timeout):
			self.timeout = timeout

	class Validate:

		def __init__(self, rule, message, num=None):
			self.rule = rule
			self.message = message
			self.num = num

	class Authenticate:

		def __init__(self, assign_to, message):
			self.assign_to = assign_to
			self.message = message