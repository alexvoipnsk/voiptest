from processor.variables_tree_builder import VariablesTreeBuilder
from processor.network import NetworkAdapter
from processor.megaco import Megaco
from processor.mgcp import Mgcp
from time import sleep, strftime
from threading import Event
from re import findall, compile as re_compile
from sre_constants import error as re_compile_error
from sys import exit
import processor.m2ua as m2ua
import processor.iua as iua
import processor.sorm268 as sorm

class ScenarioInterpreter:
	"""Class for Scenario instances interpretation"""

	_instance = None
	_global_variables_tree = None

	def _define_command_handlers(self):
		"""Defines command handlers for scenario instructions executing"""
		return { "Define" : self._handle_define,
		         "Connect": self._handle_connect,
		         "Disconnect": self._handle_disconnect,
		         "Send" : self._handle_send,
		         "Recv" : self._handle_recv,
		         "Actions" : self._handle_actions,
		         "Catch" : self._handle_catch,
		         "Compare" : self._handle_compare,
		         "Assign" : self._handle_assign,
		         "Print" : self._handle_print,
		         "Exit" : self._handle_exit,
		         "Nop" : self._handle_nop,
		         "Pause" : self._handle_pause,
		         "Validate" : self._handle_validate,
		         "GetBytes" : self._handle_getbytes }

	def __new__(cls, *args, **kwargs):
		if ScenarioInterpreter._instance is None:
			ScenarioInterpreter._instance = object.__new__(cls)
		return ScenarioInterpreter._instance

	def __init__(self, config):
		self._command_handlers = self._define_command_handlers()  # Defines scenario command handlers 
		self._network_adapters = ScenarioInterpreter._configure_adapters(config.connections, config.sock)  # Configures network adapters for defined connections
		self._routes = ScenarioInterpreter._configure_routes(config.connections)  # Configures and returns routes to connected nodes
		self._successfull_exit_flag = Event()  # Indicates successful scenario exit
		self._local_variables = None  # Local scenario namespace
		self._test_log = None         # For test log collection
		self._protocol = Megaco()     # Megaco protocol instance
		self._protocol_handlers = self._signaling_protocol_handlers()
		self._validator_handlers = self._signaling_protocol_validator_handlers()
		self._sctp_ppid = self._define_sctp_ppid()
		self.M2ua_executor = m2ua.Config_Executor()
		self.M2ua_builder = m2ua.Message_Builder()
		self.M2ua_validator = m2ua.Message_Validator()
		self.M2ua_parser = m2ua.Message_Parser()
		self.iua_executor = iua.Config_Executor()
		self.iua_builder = iua.Message_Builder()
		self.iua_validator = iua.Message_Validator()
		self.iua_parser = iua.Message_Parser()
		self.SORM_executor = sorm.Config_Executor()
		self.SORM_builder = sorm.Message_Builder()
		self.SORM_validator = sorm.Message_Validator()
		ScenarioInterpreter._global_variables_tree = VariablesTreeBuilder(config).build_tree()  # Global variables tree (Global namespace)

	def _define_sctp_ppid(self):
		"""Defines ppid values for sctp"""
		return { "iua" : 0x01000000,
		         "m2ua" : 0x02000000, 
		         "megaco" : 0x04000000 }

	def _signaling_protocol_handlers(self):
		"""Defines signaling protocol handlers"""
		return { "m2ua" : self._handle_m2ua,
				 "iua" : self._handle_iua,
				 "mgcp" : self._handle_mgcp,
		         "megaco" : self._handle_megaco,
		         "sorm" : self._handle_sorm }

	def _signaling_protocol_validator_handlers(self):
		"""Defines signaling protocol handlers"""
		return { "m2ua" : self._handle_validate_m2ua, 
				 "iua" : self._handle_validate_iua,
				 "sorm" : self._handle_validate_sorm}

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
			if connection.from_sock not in config_data:
				config_data[connection.from_sock] = [connection.id]
			else:
				config_data[connection.from_sock] += [connection.id]
		network_adapters = {}
		for key,value in config_data.items():
			network_adapters[tuple(value)] = NetworkAdapter(ScenarioInterpreter._fetch_item(key, nodes),
			*[ScenarioInterpreter._fetch_item(ScenarioInterpreter._fetch_item(i,connections).to_sock, nodes) for i in value])
		return network_adapters

	def stop_all_network_adapters(self):
		"""Closes all open network sockets"""
		for network_adapter in self._network_adapters.values():
			network_adapter.close()

	@staticmethod
	def _configure_routes(connections):
		"""Configures and returns routes to connected nodes (dictionary by the pattern "connection_id : connected_node")"""
		return dict([(connection.id, connection.to_sock) for connection in connections])

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
				string = string.replace("[$$" + variable + "]", str(value))                           # Replacing a global variable with its value
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

	def _handle_megaco(self, message):
		"""megaco protocol message handling"""
		return message

	def _handle_mgcp(self, message):
		"""megaco protocol message handling"""
		return message

	def _handle_m2ua(self, message):
		"""m2ua protocol message handling"""
		M2ua_handler = self.M2ua_builder._M2ua_make_message_handler()
		mes_type, params = self.M2ua_executor.Values_Exec(message)
		message = M2ua_handler[mes_type](**params)
		return message

	def _handle_sorm(self, message):
		"""sorm protocol message handling"""
		SORM_handler = self.SORM_builder._SORM_make_command_handler()
		print ("::FOR LOGGING PURPOSE. INTERPRETER_MODULE. SORM message handling1::",message)
		command, params = self.SORM_executor.Values_Exec(message)
		print ("::FOR LOGGING PURPOSE. INTERPRETER_MODULE. SORM message handling2::",command, params)
		message = SORM_handler[command](**params)
		return message

	def _handle_validate_sorm(self, message, data, number):
		print ("UUUUUUUU", data, number)
		validator = self.SORM_validator._SORM_check_message_handler()
		if data == "NO_MESSAGE":
			if message == "NO_MESSAGE":
				return (True, "No message received as scenario plan")
			else:
				return (False, "No message received but {0} was expected".format(message))
		if number==None:
			recvdata==data
		else:
			n=0
			b=b''
			flag=False
			for _each in data:
				if _each==204:
					n+=1
					if n==number:
						b=_each.to_bytes(1, byteorder='big')
						flag=True
					elif n<number:
						b=_each.to_bytes(1, byteorder='big')
						flag=False
					else:
						temp_recvdata=b
						flag=True
						break
				else:
					b+=_each.to_bytes(1, byteorder='big')
				temp_recvdata=b
			if flag:
				recvdata=temp_recvdata
			else:
				recvdata=b''
		mes_type, params = self.SORM_executor.Values_Exec(message)
		print ("::FOR LOGGING PURPOSE. SORM_HANDLE_VALIDATE::", mes_type, params, recvdata)
		success, info = validator[mes_type](recvdata, **params)
		return (success, info)

	def _handle_validate_m2ua(self, message, data):
		#mes_type, params = self.M2ua_validator.Params_Executor(message)
		mes_type, params = self.M2ua_executor.Values_Exec(message) # replace
		if data == "NO_MESSAGE":
			object_data = data
		else:
			object_data = self.M2ua_parser.Parse_Message(data)
		success, info = self.M2ua_validator.Validate_Message(object_data, mes_type, params)
		return (success, info)

	def _handle_iua(self, message):
		"""iua protocol message handling"""
		iua_handler = self.iua_builder._Iua_make_message_handler()
		mes_type, params = self.iua_executor.Values_Exec(message)
		message = iua_handler[mes_type](**params)
		return message

	def _handle_validate_iua(self, message, data):
		#mes_type, params = self.iua_validator.Params_Executor(message)
		mes_type, params = self.iua_executor.Values_Exec(message) # replace
		if data == "NO_MESSAGE":
			object_data = data
		else:
			object_data = self.iua_parser.Parse_Message(data)
		success, info = self.iua_validator.Validate_Message(object_data, mes_type, params)
		return (success, info)

	def _handle_define(self, instruction):
		"""Executes the define instruction of the test scenario

		Adds users variables to local scenario namespace
		"""
		self._local_variables.update(instruction.variables)
		self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Define]    User variables '%s' were successfully defined in the local namespace\n" % ", ".join(instruction.variables.keys())
		return True

	def _handle_connect(self, instruction):
		"""Executes	the connect instruction of the test scenario

		Returns True, if instruction has successfully completed or False otherwise
		"""
		# Searching for a network adapter by connection identifier
		network_adapter = self._get_network_adapter(instruction.connection)
		if network_adapter is None:
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Connect]   Value '%s' is nonexistent connection identifier\n" % instruction.connection
			return False
		# Check, connect not used with UDP proto
		if network_adapter.transport not in ("tcp", "sctp"):
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Connect]   Value '%s' is nonconsistent. Tag Connect only used with tcp or sctp transport\n" % network_adapter.proto
			return False
		# Connect logical connection to the remote node
		success, info = network_adapter.connect(to_node=self._routes[instruction.connection], mode=instruction.mode)
		self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Connect]   " +  info + "\n"
		if not success:
			return False
		return True

	def _handle_disconnect(self, instruction):
		"""Executes	the connect instruction of the test scenario

		Returns True, if instruction has successfully completed or False otherwise
		"""
		# Searching for a network adapter by connection identifier
		network_adapter = self._get_network_adapter(instruction.connection)
		if network_adapter is None:
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Disconn]   Value '%s' is nonexistent connection identifier\n" % instruction.connection
			return False
		# Check, connect not used with UDP proto
		if network_adapter.transport not in ("tcp", "sctp"):
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Disconn]   Value '%s' is nonconsistent. Tag Connect only used with tcp or sctp transport\n" % network_adapter.proto
			return False
		# Connect logical connection to the remote node
		success, info = network_adapter.close()
		self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Disconn]   " +  info + "\n"
		if not success:
			return False
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
		if instruction.sec_connection !=99999:
			network_adapter_sec = self._get_network_adapter(instruction.sec_connection)
			sec_route = network_adapter_sec._routes[self._routes[instruction.sec_connection]]
			success, recv_log, data = network_adapter.recv(self._routes[instruction.connection], timeout=instruction.timeout, sec_from_node=sec_route)
		else:
			success, recv_log, data = network_adapter.recv(self._routes[instruction.connection], timeout=instruction.timeout, sec_from_node=instruction.sec_connection)
		self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Recv]      " + recv_log + "\n"
		if not success and not data:
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
		print ("::FOR LOGGING PURPOSE. INTERPRETER_MODULE. SEND handling1::", instruction.message)
		network_adapter = self._get_network_adapter(instruction.connection)
		if network_adapter is None:
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Send]      Value '%s' is nonexistent connection identifier\n" % instruction.connection
			return False
		# Modify message with protocol handler
		# Changing variables to their values
		print ("::FOR LOGGING PURPOSE. INTERPRETER_MODULE. SEND handling2::", instruction.message)
		success, reason, temp_message = self._replace_variables(instruction.message)
		print ("::FOR LOGGING PURPOSE. INTERPRETER_MODULE. SEND handling3::", temp_message)
		message = self._protocol_handlers[network_adapter.proto](temp_message)
		if not success:
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Send]      " + reason + "\n"
			return False
		# Sending a message to the remote node
		if network_adapter.transport == "udp":
			success, info = network_adapter.send(message, to_node=self._routes[instruction.connection])
		elif network_adapter.transport == "sctp":
			success, info = network_adapter.send_sctp(message, mes_type=instruction.message, to_node=self._routes[instruction.connection], used_ppid=self._sctp_ppid[network_adapter.proto], used_stream=instruction.stream)
		elif network_adapter.transport == "tcp":
			success, info = network_adapter.send_tcp(message, to_node=self._routes[instruction.connection])
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
		if type(data) != str:
			data = data.decode()
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

	def _handle_getbytes(self, instruction, data=None):
		"""Executes the getbytes instruction of the test scenario

		Returns True, if instruction has successfully completed or False otherwise
		"""
		if data is None:
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[GetBytes]  There is no data to getbytes, you must use this instruction in the recv section\n"
			return False
		variable = instruction.assign_to
		if instruction.tobyte is not None:
			tobyte = int(instruction.tobyte)
			if tobyte > int(instruction.frombyte):
				self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[GetBytes]  ToByte is less than FromByte\n"
				return False
			else:
				databytes = data[int(instruction.frombyte):tobyte]
				print("fff", databytes)
				self._local_variables[variable] = databytes.decode()
				self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[GetBytes]  The bytes from '%s' to '%s' has been written to variable '%s'\n" % (instruction.frombyte, tobyte, instruction.assign_to)
		else: 
			databytes = data[int(instruction.frombyte):]
			print("fff1", databytes)
			self._local_variables[variable] = databytes.decode()
			self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[GetBytes]  The bytes from '%s' to last byte has been written to variable '%s'\n" % (instruction.frombyte, instruction.assign_to)
		return True

	def _handle_pause(self, instruction, *args):
		"""Executes the pause instruction of the test scenario

		Suspends the test execution for timeout duration
		"""
		sleep(instruction.timeout / 1000)
		self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Pause]     Suspended by %s milliseconds\n" % instruction.timeout
		return True

	def _handle_validate(self, instruction, data=None):
		"""Executes	the validate instruction of the test scenario

		Returns True, if instruction has successfully completed or False otherwise
		"""
		success, reason, temp_message = self._replace_variables(instruction.message)
		if instruction.rule == "m2ua":
			success, info = self._validator_handlers[instruction.rule](temp_message, data)	
		elif instruction.rule == "iua":
			success, info = self._validator_handlers[instruction.rule](temp_message, data)
		elif instruction.rule == "sorm":
			success, info = self._validator_handlers[instruction.rule](temp_message, data, instruction.num)	
		self._test_log += strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\t[Validate]  " +  info + "\n"
		if not success:
			return False
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