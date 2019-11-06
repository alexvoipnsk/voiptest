from parser.config_builder import ConfigBuilder
from jsonschema import Draft4Validator
from sys import exit
import json

class ConfigParser:
	"""Class for parsing the configuration file"""

	_instance = None

	def __new__(cls, *args, **kwargs):
		if ConfigParser._instance is None:
			ConfigParser._instance = object.__new__(cls)
		return ConfigParser._instance

	def __init__(self):
		self._validator = ConfigValidator()     # Validator for the configuration file
		self._config_builder = ConfigBuilder()  # Builder for the Config instance

	def parse_config(self, config_file):
		"""Parses the configuration file

		Returns the Config instance
		"""
		AppLogger.info("Parsing of the configuration file...")
		content = JSONWorker.fetch_content(config_file)    # Deserialization and decoding of the configuration file
		self._validator.validate_config(content)           # Validating the configuration file
		AppLogger.info("The Config instance is created [OK]")
		return self._config_builder.build_config(content)  # Makes the Config instance based on the configuration file

class ConfigValidator:
	"""Class for validating the configuration file contents"""

	# Error definition string before detail description
	_error_basis = "Configuration file is not valid. Details: "

	def __init__(self):
		# Making the schema instance for validation of the configuration file contents 
		self._schema = JSONWorker.fetch_content(FileSystem.get_current_path() + "/parser/schema/config.json") 

	def validate_config(self, content):
		"""Validates the configuration file contents according to the schema"""
		errors = sorted(Draft4Validator(self._schema).iter_errors(content), key=lambda e: e.path)
		# Checking for errors when validating
		# If the error is caught, makes the error exit
		if errors:
			ConfigValidator._print_errors(errors)
			exit(1)
		# Checking the existence and availability of a directory for logs
		if not FileSystem.is_acceptable_directory(content["LogDirectory"]):
			AppLogger.error(ConfigValidator._error_basis + "unacceptable log directory '%s' " % content["LogDirectory"])
			exit(1)
		# Checking the uniqueness of nodes and connections identifiers
		ConfigValidator._has_unique_identiers(Nodes=content["Nodes"], Connections=content["Connections"])
		# Checking for the absence of degenerate connections
		ConfigValidator._has_acceptable_connections(content["Connections"])

	@staticmethod
	def _has_unique_identiers(**sections):
		"""Checks for uniqueness of nodes and connections identifiers

		Nodes and connections identifiers must be unique within its own section
		Makes the error exit if the condition above is False
		"""
		identifiers = set()
		for name, section in sections.items():
			identifiers.clear()
			for item in section:
				if item["id"] not in identifiers:
					identifiers.add(item["id"])
				else:
					AppLogger.error(ConfigValidator._error_basis + "object with id '%s' in section '%s' has a non-unique identifier: '%s'" % (item["id"], name, item["id"]))
					exit(1)

	@staticmethod
	def _has_acceptable_connections(connections):
		"""Checks for the absence of degenerate connections

		from_node and to_node properties of connection should't be equal
		Makes the error exit if the condition above is False
		"""
		for connection in connections:
			if connection["from_node"] == connection["to_node"]:
				AppLogger.error(ConfigValidator._error_basis + "connection with id '%s' has an equal node identifiers in 'from_node' and 'to_node' properties" % connection["id"])
				exit(1)

	@staticmethod
	def _print_errors(errors):
		"""Prints errors found during the configuration validation"""
		for error in errors:
			if len(error.path) == 0:
				AppLogger.error(ConfigValidator._error_basis + error.message)
			elif len(error.path) == 1 or len(error.path) == 2:
				AppLogger.error(ConfigValidator._error_basis + "%s in section '%s'" % (error.message, error.path[0]))
			elif len(error.path) == 3:
				AppLogger.error(ConfigValidator._error_basis + "%s in section '%s' property '%s'" % (error.message, error.path[0], error.path[-1]))
			else:
				AppLogger.error(ConfigValidator._error_basis + "%s in section '%s' property '%s'" % (error.message, error.path[0], error.path[-2]))

class JSONWorker:
	"""Static class for parsing json contents"""

	@staticmethod
	def decode_json(content):
		"""Decodes json contents"""
		try:
			decoded_content = json.loads(content)
		except json.decoder.JSONDecodeError as error:
			AppLogger.error("Can't parse the configuration file. Details: %s" % error)
			exit(1)
		return decoded_content

	@staticmethod
	def fetch_content(file):
		"""Loads and decodes the contents of the json file

		Returns decoded json contents or makes the error exit
		"""
		file_content = FileSystem.load_from(file, binary=False)
		if file_content is None:
			AppLogger.error("Can't load the configuration file from path '%s'. Details: file does't exist or no permission to read it" % file)
			exit(1)
		content = JSONWorker.decode_json(file_content)
		return content