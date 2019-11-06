class VariablesTreeBuilder:
	"""Class for building the VariableTree instance from the configuration file info"""

	_instance = None

	def __new__(cls, *args, **kwargs):
		if VariablesTreeBuilder._instance is None:
			VariablesTreeBuilder._instance = object.__new__(cls)
		return VariablesTreeBuilder._instance

	def __init__(self, config):
		self.config = config                  # Config instanse
		self._var_tree = VariableTree()       # VariableTree instanse
		self._makers = self._define_makers()  # Makers for building the VariableTree instance
		self._protocols = self._define_protocols() # Protocol sections in configuration

	def _define_makers(self):
		"""Defines makers for building the VariableTree instance"""
		return {
		    "Globals" : self._make_globals,
		    "Dialplans" : self._make_dialplans,
		    "sock" : self._make_socks,
		    "name" : self._make_name,
		    "ipaddr" : self._make_ip_address,
		    "port" : self._make_port,
		    "transport" : self._make_transport,
		    "proto" : self._make_proto,
		    "profile" : self._make_profile,
		    "mid" : self._make_mid,
		    "encoding" : self._make_encoding,
		    "network_buffer" : self._make_network_buffer,
		    "terms" : self._make_terms,
		    "asp" : self._make_asp,
		    "iid" : self._make_iid
		}

	def _define_protocols(self):
		"""Defines protocol sections"""
		return {
			"megaco" : self.config.megaco,
			"sigtran" : self.config.sigtran,
			"mgcp" : self.config.mgcp
		}

	def _make_globals(self, section):
		"""Builds VariableTree nodes from Globals section of the configuration file"""
		for variable, value in section.items():
			self._var_tree.childs.append(VariableTree.TreeNode(variable, value))

	def _make_dialplans(self, section):
		"""Builds VariableTree nodes from Dialplans section of the configuration file"""
		dialplans = VariableTree.TreeNode("Dialplans")
		for number, value in enumerate(section):
			dialplans.childs.append(VariableTree.TreeNode(str(number), value))
		self._var_tree.childs.append(dialplans)

	def _make_socks(self, section):
		"""Builds VariableTree nodes from Nodes section of the configuration file"""
		socks = VariableTree.TreeNode("sock")
		for sock in section:
			socks.childs.append(self._make_sock(sock))
		self._var_tree.childs.append(socks)

	def _make_sock(self, fabric):
		"""Builds and returns VariableTree node from specific Node properties"""
		sock = VariableTree.TreeNode(str(fabric.id))
		protocol = None
		for parameter, value in fabric.__dict__.items():
			if ((parameter == "profile") and protocol):
				if ((protocol == "m2ua") or (protocol == "iua")):
					protocol = "sigtran"
				sock = self._makers[parameter](self._protocols[protocol], value, sock)
			elif (parameter != "id"):
				if parameter == "proto":
					protocol = value
				sock.childs.append(self._makers[parameter](value))
		return sock

	def _make_name(self, value):
		"""Builds and returns VariableTree node from the name of the specific Node"""
		return VariableTree.TreeNode("name", value)

	def _make_ip_address(self, value):
		"""Builds and returns VariableTree node from the ip_address of the specific Node"""
		return VariableTree.TreeNode("ipaddr", value)

	def _make_port(self, value):
		"""Builds and returns VariableTree node from the port of the specific Node"""
		return VariableTree.TreeNode("port", str(value))

	def _make_transport(self, value):
		"""Builds and returns VariableTree node from the transport of the specific Node"""
		return VariableTree.TreeNode("transport", str(value))

	def _make_proto(self, value):
		"""Builds and returns VariableTree node from the proto of the specific Node"""
		return VariableTree.TreeNode("proto", str(value))		

	def _make_profile(self, fabric, ident, tree):
		"""Builds and returns VariableTree node from specific Node properties"""
		for section in fabric:
			if section.id == ident:
				for parameter, value in section.__dict__.items():
					if parameter != "id":
						tree.childs.append(self._makers[parameter](value))
		return tree

	def _make_mid(self, value):
		"""Builds and returns VariableTree node from the mid of the specific Node """
		return VariableTree.TreeNode("mid", value)

	def _make_encoding(self, value):
		"""Builds and returns VariableTree node from the encoding of the specific Node"""
		return VariableTree.TreeNode("encoding", value)

	def _make_network_buffer(self, value):
		"""Builds and returns VariableTree node from the network_buffer of the specific Node"""
		return VariableTree.TreeNode("network_buffer", str(value))

	def _make_terms(self, fabric):
		"""Builds and returns VariableTree node from terms of the specific Node"""
		terms = VariableTree.TreeNode("terms")
		for number, value in enumerate(fabric):
			terms.childs.append(VariableTree.TreeNode(str(number), value))
		return terms

	def _make_asp(self, fabric):
		"""Builds and returns VariableTree node from asp of the specific Node"""
		asp = VariableTree.TreeNode("asp")
		for number, value in enumerate(fabric):
			asp.childs.append(VariableTree.TreeNode(str(number), value))
		return asp

	def _make_iid(self, fabric):
		"""Builds and returns VariableTree node from iid of the specific Node"""
		iid = VariableTree.TreeNode("iid")
		for number, value in enumerate(fabric):
			iid.childs.append(VariableTree.TreeNode(str(number), value))
		return iid

	def build_tree(self):
		"""Builds and returns the VariableTree instance"""
		for name, section in {"Globals" : self.config.globals, 
		                      "Dialplans" : self.config.dialplans, 
		                      "sock" : self.config.sock}.items():
			self._makers[name](section)  # Building the VariableTree instance 
		return self._var_tree

class VariableTree:
	
	def __init__(self):
		self.childs = []

	class TreeNode:

		def __init__(self, identifier, value=None):
		    self.identifier = identifier
		    self.value = value
		    self.childs = [] if value is None else None

		def __repr__(self):
			return "TreeNode: %s" % self.identifier

	def get_variable(self, path, subtree=None):
		subtree = subtree if subtree else self.childs
		segment = path[0]                  
		for child in subtree:
			if child.identifier == segment:
				if child.value is None:
					if len(path) != 1:             
						return self.get_variable(path[1:], subtree=child.childs)
				elif len(path) == 1:                
					return child.value