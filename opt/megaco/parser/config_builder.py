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
		        "Connections" : self._make_connections,
		        "sock" : self._make_sock,
		        "megaco" : self._make_megaco,
		        "mgcp" : self._make_mgcp,
		        "sigtran" : self._make_sigtran}

	@staticmethod
	def _build_connection(fabric):
		"""Builds and returns the Connection instance"""
		connection = Config.Connection(fabric["id"], fabric["from_sock"], fabric["to_sock"])  # Builds the required attributes of the Connection instance
		try:                                                                                  # Builds optional attributes of the Connection instance
			connection.name = fabric["name"]
		except KeyError:
			pass
		return connection

	@staticmethod
	def _build_sock(fabric):
		"""Builds and returns the sock instance"""
		socket = Config.Sock(fabric["id"], fabric["ipaddr"], fabric["port"], fabric["transport"], fabric["proto"])  # Builds the required attributes of the sock instance
		for field in ("name", "profile", "network_buffer"):    # Builds optional attributes of the sock instance
			try:
				if field == "name":
					socket.name = fabric[field]
				elif field == "profile":
					socket.profile = fabric[field]
				elif field == "network_buffer":
					socket.network_buffer = fabric[field]
				elif field == "proto_type":
					socket.proto_type = fabric[field]
			except KeyError:
				pass
		return socket

	@staticmethod
	def _build_megaco(fabric):
		"""Builds and returns the megaco instance"""
		megaco = Config.Megaco(fabric["id"], fabric["mid"])  # Builds the required attributes of the megaco instance
		for field in ("encoding", "terms"):    # Builds optional attributes of the megaco instance
			try:
				if field == "encoding":
					megaco.encoding = fabric[field]
				elif field == "terms":
					megaco.terms = tuple(fabric[field])
			except KeyError:
				pass
		return megaco

	@staticmethod
	def _build_mgcp(fabric):
		"""Builds and returns the megaco instance"""
		mgcp = Config.Mgcp(fabric["id"], fabric["mid"])  # Builds the required attributes of the megaco instance
		for field in ("encoding", "terms"):    # Builds optional attributes of the megaco instance
			try:
				if field == "encoding":
					mgcp.encoding = fabric[field]
				elif field == "terms":
					mgcp.terms = tuple(fabric[field])
			except KeyError:
				pass
		return mgcp

	@staticmethod
	def _build_sigtran(fabric):
		"""Builds and returns the sigtran instance"""
		sigtran = Config.Sigtran(fabric["id"])  # Builds the required attributes of the sigtran instance
		for field in ("asp", "iid"):    # Builds optional attributes of the sigtran instance
			try:
				if field == "asp":
					sigtran.asp = tuple(fabric[field])
				elif field == "iid":
					sigtran.iid = tuple(fabric[field])
			except KeyError:
				pass
		return sigtran

	def _make_log_directory(self, sample):
		"""Builds the lod_dir attribute of the Config instance"""
		self._config.log_dir = sample

	def _make_globals(self, sample):
		"""Builds the globals attribute of the Config instance"""
		self._config.globals = sample

	def _make_dialplans(self, sample):
		"""Builds the dialplans attribute of the Config instance"""
		self._config.dialplans = sample

	def _make_connections(self, sample):
		"""Builds the connections attribute of the Config instance"""
		self._config.connections = tuple(ConfigBuilder._build_connection(fabric) for fabric in sample)

	def _make_sock(self, sample):
		"""Builds the sock attribute of the Config instance"""
		self._config.sock = tuple(ConfigBuilder._build_sock(fabric) for fabric in sample)
		
	def _make_megaco(self, sample):
		"""Builds the megaco attribute of the Config instance"""
		self._config.megaco = tuple(ConfigBuilder._build_megaco(fabric) for fabric in sample)

	def _make_mgcp(self, sample):
		"""Builds the mgcp attribute of the Config instance"""
		self._config.mgcp = tuple(ConfigBuilder._build_mgcp(fabric) for fabric in sample)

	def _make_sigtran(self, sample):
		"""Builds the sigtran attribute of the Config instance"""
		self._config.sigtran = tuple(ConfigBuilder._build_sigtran(fabric) for fabric in sample)

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
		self.connections = None
		self.sock = None
		self.user = None
		self.device = None
		self.sigtran = None
		self.megaco = None
		self.mgcp = None

	class Connection:

		def __init__(self, conn_id, from_sock, to_sock):
			self.id = conn_id
			self.name = ""
			self.from_sock = from_sock
			self.to_sock = to_sock

	class Sock:

		def __init__(self, node_id, ip_address, port, transport, proto):
			self.id = node_id
			self.name = ""
			self.ipaddr = ip_address
			self.port = port
			self.transport = transport
			self.proto = proto
			self.profile = None
			self.network_buffer = 15000

	class Megaco:

		def __init__(self, node_id, mident):
			self.id = node_id
			self.mid = mident
			self.encoding = "full_text"
			self.terms = tuple()

	class Sigtran:

		def __init__(self, node_id):
			self.id = node_id
			self.asp = tuple()
			self.iid = tuple()

	class Mgcp:

		def __init__(self, node_id, mident):
			self.id = node_id
			self.mid = mident
			self.encoding = "full_text"
			self.terms = tuple()