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
		        "sorm" : self._make_sorm,
		        "sip" : self._make_sip,
		        "users" : self._make_users,
		        "trunks" : self._make_trunks,
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
		for field in ("name", "profile", "network_buffer", "proto_type"):    # Builds optional attributes of the sock instance
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
		"""Builds and returns the mgcp instance"""
		mgcp = Config.Mgcp(fabric["id"], fabric["mid"])  # Builds the required attributes of the mgcp instance
		for field in ("encoding", "terms"):    # Builds optional attributes of the mgcp instance
			try:
				if field == "encoding":
					mgcp.encoding = fabric[field]
				elif field == "terms":
					mgcp.terms = tuple(fabric[field])
			except KeyError:
				pass
		return mgcp

	@staticmethod
	def _build_sorm(fabric):
		"""Builds and returns the SORM instance"""
		sorm = Config.Sorm(fabric["id"], fabric["ormNum"], fabric["password"], fabric["version"], fabric["station_type"])  # Builds the required attributes of the sorm instance
		return sorm

	@staticmethod
	def _build_sip(fabric):
		"""Builds and returns the SORM instance"""
		sip = Config.Sip(fabric["id"], fabric["auth"])  # Builds the required attributes of the sorm instance
		return sip

	@staticmethod
	def _build_users(fabric):
		"""Builds and returns the users instance"""
		users = Config.Users(fabric["id"], fabric["username"])  # Builds the required attributes of the users instance
		for field in ("authname", "password", "domain", "service", "servicelist"):    # Builds optional attributes of the users instance
			try:
				if field == "authname":
					users.authname = fabric[field]
				elif field == "password":
					users.password = fabric[field]
				elif field == "domain":
					users.domain = fabric[field]
				elif field == "service":
					users.service = tuple(fabric[field])
				elif field == "servicelist":
					users.servicelist = tuple(fabric[field])
			except KeyError:
				pass
		return users

	@staticmethod
	def _build_trunks(fabric):
		"""Builds and returns the trunks instance"""
		trunks = Config.Trunks(fabric["id"], fabric["name"])  # Builds the required attributes of the trunks instance
		for field in ("authname", "password", "domain", "number"):    # Builds optional attributes of the users instance
			try:
				if field == "authname":
					trunks.authname = fabric[field]
				elif field == "password":
					trunks.password = fabric[field]
				elif field == "domain":
					trunks.domain = fabric[field]
				elif field == "number":
					trunks.number = fabric[field]
			except KeyError:
				pass
		return trunks

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

	def _make_sorm(self, sample):
		"""Builds the sorm attribute of the Config instance"""
		self._config.sorm = tuple(ConfigBuilder._build_sorm(fabric) for fabric in sample)

	def _make_sip(self, sample):
		"""Builds the sip attribute of the Config instance"""
		self._config.sip = tuple(ConfigBuilder._build_sip(fabric) for fabric in sample)

	def _make_users(self, sample):
		"""Builds the users attribute of the Config instance"""
		self._config.users = tuple(ConfigBuilder._build_users(fabric) for fabric in sample)

	def _make_trunks(self, sample):
		"""Builds the trunks attribute of the Config instance"""
		self._config.trunks = tuple(ConfigBuilder._build_trunks(fabric) for fabric in sample)

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
		self.users = None
		self.trunks = None
		self.device = None
		self.sigtran = None
		self.megaco = None
		self.sip = None
		self.mgcp = None
		self.sorm = None

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

	class Sorm:

		def __init__(self, node_id, ormNum_id, password, version, station_type):
			self.id = node_id
			self.ormNum = ormNum_id
			self.password = password
			self.version = version
			self.station_type = station_type

	class Sip:

		def __init__(self, node_id, auth=1):
			self.id = node_id
			self.auth = auth

	class Users:

		def __init__(self, node_id, username, authname = None, password = None, domain = None, service = None, servicelist = None):
			self.id = node_id
			self.username = username
			self.authname = authname
			self.password = password
			self.domain = domain
			self.service = tuple()
			self.servicelist = tuple()

	class Trunks:

		def __init__(self, node_id, name, authname = None, password = None, domain = None, number = None):
			self.id = node_id
			self.name = name
			self.authname = authname
			self.password = password
			self.domain = domain
			self.number = number