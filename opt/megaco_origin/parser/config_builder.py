class ConfigBuilder:
	"""Class for building the Config instance from validated contents of the configuration file"""

	_instance = None

	def __new__(cls, *args, **kwargs):
		if ConfigBuilder._instance is None:
			ConfigBuilder._instance = object.__new__(cls)
		return ConfigBuilder._instance

	def __init__(self):
		self._config = Config()               # Config instance
		self._makers = self._define_makers()  # Makers for building the Config instance

	def _define_makers(self):
		"""Defines makers for building the Config instance"""
		return {"LogDirectory" : self._make_log_directory,
		        "Globals" : self._make_globals,
		        "Dialplans" : self._make_dialplans,
		        "Nodes" : self._make_nodes,
		        "Connections" : self._make_connections}

	@staticmethod
	def _build_node(fabric):
		"""Builds and returns the Node instance"""
		node = Config.Node(fabric["id"], fabric["ip_address"], fabric["port"])  # Builds the required attributes of the Node instance
		for field in ("name", "mid", "encoding", "terms", "network_buffer"):    # Builds optional attributes of the Node instance
			try:
				if field == "name":
					node.name = fabric[field]
				elif field == "mid":
					node.mid = fabric[field]
				elif field == "encoding":
					node.encoding = fabric[field]
				elif field == "terms":
					node.terms = tuple(fabric[field])
				elif field == "network_buffer":
					node.network_buffer = fabric[field]
			except KeyError:
				pass
		return node

	@staticmethod
	def _build_connection(fabric):
		"""Builds and returns the Connection instance"""
		connection = Config.Connection(fabric["id"], fabric["from_node"], fabric["to_node"])  # Builds the required attributes of the Connection instance
		try:                                                                                  # Builds optional attributes of the Connection instance
			connection.name = fabric["name"]
		except KeyError:
			pass
		return connection

	def _make_log_directory(self, sample):
		"""Builds the lod_dir attribute of the Config instance"""
		self._config.log_dir = sample

	def _make_globals(self, sample):
		"""Builds the globals attribute of the Config instance"""
		self._config.globals = sample

	def _make_dialplans(self, sample):
		"""Builds the dialplans attribute of the Config instance"""
		self._config.dialplans = sample

	def _make_nodes(self, sample):
		"""Builds the nodes attribute of the Config instance"""
		self._config.nodes = tuple(ConfigBuilder._build_node(fabric) for fabric in sample)

	def _make_connections(self, sample):
		"""Builds the connections attribute of the Config instance"""
		self._config.connections = tuple(ConfigBuilder._build_connection(fabric) for fabric in sample)

	def build_config(self, content):
		"""Builds and returns the Config instance"""
		for component in content:
			self._makers[component](content[component])   # Building the Config attributes 
		return self._config

class Config:

	def __init__(self):
		self.log_dir = None
		self.globals = {}
		self.dialplans = []
		self.nodes = None
		self.connections = None

	class Node:

		def __init__(self, node_id, ip_address, port):
			self.id = node_id
			self.name = ""
			self.ip_address = ip_address
			self.port = port
			self.mid = "[%s]:%s" % (self.ip_address, self.port)
			self.encoding = "full_text"
			self.terms = tuple()
			self.network_buffer = 15000

	class Connection:

		def __init__(self, conn_id, from_node, to_node):
			self.id = conn_id
			self.name = ""
			self.from_node = from_node
			self.to_node = to_node