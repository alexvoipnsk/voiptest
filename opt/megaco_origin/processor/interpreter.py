from processor.variables_tree_builder import VariablesTreeBuilder
from processor.network import NetworkAdapter
from processor.megaco import Megaco
from time import sleep, strftime
from threading import Event
from re import findall, compile as re_compile
from sre_constants import error as re_compile_error
from sys import exit

class ScenarioInterpreter:
	"""Class for Scenario instances interpretation"""

	_instance = None
	_global_variables_tree = None

	def _define_command_handlers(self):
		"""Defines command handlers for scenario instructions executing"""
		return { "Define" : self._handle_define,
		         "Send" : self._handle_send,
		         "Recv" : self._handle_recv,
		         "Actions" : self._handle_actions,
		         "Catch" : self._handle_catch,
		         "Compare" : self._handle_compare,
		         "Assign" : self._handle_assign,
		         "Print" : self._handle_print,
		         "Exit" : self._handle_exit,
		         "Nop" : self._handle_nop,
		         "Pause" : self._handle_pause }

	def __new__(cls, *args, **kwargs):
		if ScenarioInterpreter._instance is None:
			ScenarioInterpreter._instance = object.__new__(cls)
		return ScenarioInterpreter._instance

	def __init__(self, config):
		self._command_handlers = self._define_command_handlers()  # Defines scenario command handlers 
		self._network_adapters = ScenarioInterpreter._configure_adapters(config.connections, config.nodes)  # Configures network adapters for defined connections
		self._routes = ScenarioInterpreter._configure_routes(config.connections)  # Configures and returns routes to connected nodes
		self._successfull_exit_flag = Event()  # Indicates successful scenario exit
		self._local_variables = None  # Local scenario namespace
		self._test_log = None         # For test log collection
		self._protocol = Megaco()     # Megaco protocol instance
		ScenarioInterpreter._global_variables_tree = VariablesTreeBuilder(config).build_tree()  # Global variables tree (Global namespace)

	@staticmethod
	def _fetch_item(node_id, items):
		"""Searchs for and returns Node instance specified by node_id"""
		for item in items:
			if item.id == node_id:
				break
		else:
			AppLogger.error("Node instance with id='%s' defined in 'Connections' is not exist in 'Nodes' section" % node_id)
			exit(1)
		return item

	@staticmethod
	def _configure_adapters(connections, nodes):
		"""Configures network adapters for defined connections by pattern (connections_id tuple) : adapter"""
		config_data = {}
		for connection in connections:
			if connection.from_node not in config_data:
				config_data[connection.from_node] = [connection.id]
			else:
				config_data[connection.from_node] += [connection.id]
		network_adapters = {}
		for key,value in config_data.items():
			network_adapters[tuple(value)] = NetworkAdapter(ScenarioInterpreter._fetch_item(key, nodes),
			*[ScenarioInterpreter._fetch_item(ScenarioInterpreter._fetch_item(i,connections).to_node, nodes) for i in value])
		return network_adapters

	def stop_all_network_adapters(self):
		"""Closes all open network sockets"""
		for network_adapter in self._network_adapters.values():
			network_adapter.close()

	@staticmethod
	def _configure_routes(connections):
		"""Configures and returns routes to connected nodes (dictionary by the pattern "connection_id : connected_node")"""
		return dict([(connection.id, connection.to_node) for connection in connections])

	def _get_network_adapter(self, connection):
		"""Searches for and returns an instance of the network adapter by it's connection identifier"""
		for connections in self._network_adapters:
			if connection in connections:
				return self._network_adapters[connections]

	@staticmethod
	def _replace_global_variables(string):
		"""Replaces global variables in the string with their values

		Returns the changing result, error reason and string with replased variables (if result is True, None otherwise)
		"""
		for variable in set([var[3:-1] for var in findall(r"\[\$\$[A-Za-z0-9_.]+\]", string)]):  # Forming the set of global variables found in a string
			value = ScenarioInterpreter._global_variables_tree.get_variable(variable.split("."))
			if value is not None:
				string = string.replace("[$$" + variable + "]", value)                           # Replacing a global variable with its value
			else:
				return (False, "Variable '%s' does not exist in the global namespace" % variable, None)
		return (True, None, string)

	def _replace_protocol_variables(self, string):
		"""Replaces protocol variable in the string with their values

		Returns the changing result, error reason and string with replased variables (if result is True, None otherwise)
		"""
		for variable in set([var[3:-3] for var in findall(r"\[\$\$[A-Za-z0-9_]+\$\$\]", string)]):
			value = self._protocol.generate_value(variable)               # Forming the set of local variables with their values found in a string
			if value is not None:
				string = string.replace("[$$" + variable + "$$]", value)  # Replacing a protocol variable with its value
				self._local_variables["last_" + variable] = value         # Add protocol variable with the "last_" prefix to local scenario namespace
			else:
				return (False, "Variable '%s' is not supported by Megaco protocol" % variable, None)
		return (True, None, string)

	def _replace_local_variables(self, string):
		"""Replaces local variables in the string with their values

		Returns the changing result, error reason and string with replased variables (if result is True, None otherwise)
		"""
		for variable in set([var[2:-1] for var in findall(r"\[\$[A-Za-z0-9_]+\]", string)]):     # Forming the set of local variables found in a string
			if variable in self._local_variables:
				string = string.replace("[$" + variable + "]", self._local_variables[variable])  # Replacing a local variable with its value
			else:
				return (False, "Variable '%s' does not exist in the local namespace" % variable, None)
		return (True, None, string)

	def _replace_variables(self, string):
		"""Replaces local and global variables in the string with their values

		Returns the changing result, error reason and string with replased variables (if result is True, None otherwise)
		"""
		success, reason, string = self._replace_local_variables(string)                  # Replacing variables from the local namespace
		if not success:
			return (False, reason, None)
		success, reason, string = self._replace_protocol_variables(string)
		if not success:
			return (False, reason, None)
		success, reason, string = ScenarioInterpreter._replace_global_variables(string)  # Replacing variables from	the global namespace
		if not success:
			return (False, reason, None)
		return (True, None, string)

	def _handle_define(self, instruction):
		"""Executes the define instruction of the test scenario

		Adds users variables to local scenario namespace
		"""
		self._local_variables.update(instruction.variables)
		self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Define]    User variables '%s' were successfully defined in the local namespace\n" % ", ".join(instruction.variables.keys())
		return True

	def _handle_recv(self, instruction):
		"""Executes the recv instruction of the test scenario

		Returns True, if instruction has successfully completed or False otherwise 
		"""
		# Searching for a network adapter by connection identifier
		network_adapter = self._get_network_adapter(instruction.connection)
		if network_adapter is None:
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Recv]      Value '%s' is nonexistent connection identifier\n" % instruction.connection
			return False
		# Receiving a message from a connection
		success, recv_log, data = network_adapter.recv(self._routes[instruction.connection], timeout=instruction.timeout)
		self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Recv]      " + recv_log + "\n"
		if not success:
			return False
		# Executing nested instructions
		if not self._handle_actions(instruction.instructions, data):
			return False
		return True

	def _handle_send(self, instruction):
		"""Executes	the send instruction of the test scenario

		Returns True, if instruction has successfully completed or False otherwise
		"""
		# Searching for a network adapter by connection identifier
		network_adapter = self._get_network_adapter(instruction.connection)
		if network_adapter is None:
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Send]      Value '%s' is nonexistent connection identifier\n" % instruction.connection
			return False
		# Changing variables to their values
		success, reason, message = self._replace_variables(instruction.message)
		if not success:
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Send]      " + reason + "\n"
			return False
		# Sending a message to the remote node
		success, info = network_adapter.send(message, to_node=self._routes[instruction.connection])
		self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Send]      " +  info + "\n"
		if not success:
			return False
		return True

	def _handle_actions(self, instructions, data=None):
		"""Executes instructions from the action block

		If the command result is False, the handler terminates the scenario execution and returns False
		Returns True otherwise 
		"""
		for instruction in instructions:
			if not self._command_handlers[instruction.__class__.__name__](instruction, data):
				return False
		return True

	def _handle_catch(self, instruction, data=None):
		"""Executes the catch instruction of the test scenario

		Returns True, if instruction has successfully completed or False otherwise
		"""
		if data is None:
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Catch]     There is no data to catch, you must use this instruction in the recv section\n"
			return False
		# Compiling the regular expression
		try:
			instruction.regexp = re_compile(instruction.regexp)
		except re_compile_error as error:
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Catch]     There is an error in the regular expression \"%s\"- %s\n" % (instruction.regexp, str(error))
			return False
		# Finding all possible matches with the regular expression
		matches = instruction.regexp.findall(data)
		# Choosing the right match
		try:
			match = matches[instruction.match]
		except IndexError:
		    self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Catch]     There is no rigth match to regexp %s\n" % str(instruction.regexp)[11:-1]
		    return False
		# Splitting the variables string into words
		variables = instruction.assign_to.split(",")
		if type(match) == tuple:
			if len(match) != len(variables):
				self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Catch]     The number of values in the match group '%s' is not equal to the number of values in the assign_to group '%s'\n" % (len(match), len(variables))
				return False
		elif len(variables) != 1:
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Catch]     The number of values in the match group '1' is not equal to the number of values in the assign_to group '%s'\n" % len(variables)
			return False
		# Declaring variables in the local scenario namespace
		for number, variable in enumerate(variables):
			if type(match) == tuple:
				self._local_variables[variable] = match[number]
			else:
				self._local_variables[variable] = match
		self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Catch]     The match groups '%s' has been written to variables '%s'\n" % (str(match), ", ".join(variables))
		return True

	def _handle_pause(self, instruction, *args):
		"""Executes the pause instruction of the test scenario

		Suspends the test execution for timeout duration
		"""
		sleep(instruction.timeout / 1000)
		self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Pause]     Suspended by %s milliseconds\n" % instruction.timeout
		return True

	def _handle_nop(self, instructions):
		"""Executes the action instruction without binding to Megaco protocol

		If the result of execution of the action block is False, the handler terminates the scenario execution and returns False
		Returns True otherwise
		"""
		if not self._handle_actions(instructions.instructions):
			return False
		return True

	def _handle_compare(self, instruction, *args):
		"""Executes the compare instruction of the test scenario

		Returns True, if instruction has successfully completed or False otherwise
		"""
		success, reason, first = self._replace_variables(instruction.first)    # Changing variables to their values
		if not success:
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Compare]   " + reason + "\n"
			return False
		success, reason, second = self._replace_variables(instruction.second)  # Changing variables to their values
		if not success:
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Compare]   " + reason + "\n"
			return False
		# Splitting the strings into words
		first, second = first.split(","), second.split(",")
		if len(first) != len(second):
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Compare]   The number of values in first group '%s' is not equal to the number of values in second group '%s'\n" % (len(first), len(second))
			return False
		# Pairwise values comparison
		for number in range(len(first)):
			if first[number] != second[number]:
				self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Compare]   The value '%s' of the variable '%s' is not equal to the value '%s' of the variable '%s'\n" % (first[number], instruction.first.split(",")[number], second[number], instruction.second.split(",")[number])
				# Executing nested instructions under the inequality of compared variables
				for action in instruction.instructions:
					if not self._command_handlers[action.__class__.__name__](action):
						return False
				return True
		self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Compare]   Values from the first group are absolutely equal to values from the second group\n"
		return True

	def _handle_assign(self, instruction, *args):
		"""Executes the assign instruction of the test scenario

		Returns True, if instruction has successfully completed or False otherwise
		"""
		success, reason, values = self._replace_variables(instruction.values)     
		if not success:
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Assign]    " + reason + "\n"
			return False
		variables, values = instruction.to.split(","), values.split(",")          # Splitting the strings into words
		if len(variables) != len(values):
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Assign]    The number of assignable values '%s' is not equal to the number of declared variables '%s'\n" % (len(values), len(variables))
			return False
		for number, variable in enumerate(variables):                             # Declaring variables in the local scenario namespace
			self._local_variables[variable] = values[number]
		self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Assign]    User variables '%s' were successfully defined in the local namespace\n" % ", ".join(variables)
		return True

	def _handle_print(self, instruction, *args):
		"""Executes the print instruction of the test scenario

		Returns True, if instruction has successfully completed or False otherwise
		"""
		success, reason, text = self._replace_variables(instruction.text)  # Changing variables to their values
		if not success:
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Print]     " + reason + "\n"
			return False
		self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Print]     " +  text + "\n"
		return True

	def _handle_exit(self, instruction, *args):
		"""Executes the exit instruction of the test scenario"""
		if instruction.status == "success":
			self._successfull_exit_flag.set()                                  # Note that the output is successful
		if instruction.info is not None:
			success, reason, info = self._replace_variables(instruction.info)  # Changing variables to their values
			if not success:
				self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Exit]      " + reason + "\n"
			else:
				self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Exit]      " + info + "\n"
		return False

	def execute(self, scenario):
		"""Executes the test scenario

		Returns the execution result, collected test log and dump of messages
		"""
		self._local_variables = {}             # Setting up a local scenario namespace
		self._successfull_exit_flag.clear()    # Resetting of the successful exit flag
		self._test_log = ""                    # Initializing the test log
		# Execution of the scenario instructions
		for instruction in scenario:
			if not self._command_handlers[instruction.__class__.__name__](instruction):
				# Test result is True, if the exit status is successful 
				if self._successfull_exit_flag.isSet():
					return (True, self._test_log)
				else:
					return (False, self._test_log)
		return (True, self._test_log)