from random import randint
from time import strftime
import hashlib

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

	@staticmethod
	def _digest_auth(self, auth_data):
		if auth_data["auth_type"]==Digest:
			if auth_data["algorithm"]=="MD5":
				digest = hashlib.md5()
				A1md5 = hashlib.md5()
				A2md5 = hashlib.md5()
				A1md5.update(auth_data["authname"] + ":" + auth_data["realm"] + ":" + auth_data["password"])
				if auth_data["qop"]:
					if auth_data["qop"]=="auth":
						A2md5.update(auth_data["method"] + ":" + auth_data["digest_uri_value"])
					elif auth_data["qop"]=="auth-int":
						raise SIP_Error("AUTH: qop=auth-int isn't supported now")
						#A2 = method ":" digest_uri_value ":" H(entity-body)
					request_digest  = '"' + digest.update(A1md5 + ":" + auth_data["nonce-value"] + ":" + auth_data["nc-value"]
            	                             + ":" + auth_data["cnonce-value"] + ":" + auth_data["qop"] + ":" + A2md5) + '"'
				else:
					A2md5.update(auth_data["method"] + ":" + auth_data["digest_uri_value"])
					request_digest  = '"' + digest.update(A1md5 + ":" + auth_data["nonce-value"] + ":" + A2md5) + '"'
			elif auth_data["algorithm"]=="MD5-sess":
				raise SIP_Error("AUTH: Only MD5 alorithm is supported")
				#A1 = H( unq(username-value) ":" unq(realm-value) + ":" + passwd ) + ":" + unq(nonce-value) + ":" + unq(cnonce-value)
			else:
				raise SIP_Error("AUTH: Only MD5 or MD5-sess alorithms are supported")
			return request_digest
		else:
			raise SIP_Error("AUTH: Only Digest authentication is supported")

		#realm="dima", nonce="918d004f120b200d50e199de8a3cec8a", algorithm=MD5

		def authValuesExec(self, auth_row):
			# Ecexute auth data
			print ("::FOR LOGGING PURPOSE. SIP_AUTH_FUNCTION. Start of parsing, raw data from file::",auth_row)
			auth_params = dict()
			if auth_row:
				auth_row = auth_row.strip()
				temp_string = '' 	#temporary string for build new param value
				param = ''      	#temporary string for build new param
				for _val in auth_row:
					if _val == "'" or _val == '"':
						pass
					elif _val == ",":
						fin_string = temp_string.strip()
						if fin_string:
							try:
								fin_string = int(temp_string.strip())
							except:
								pass
							auth_params[param] = fin_string
							param = ''
						else:
							raise SIP_Error("AUTH: No parameter's value received")
					elif _val == "=":
						param = temp_string.strip().lower()
						temp_string = ''
					else:
						temp_string +=_val
				if param and temp_string:
					fin_string = temp_string.strip()
					if fin_string:
						try:
							fin_string = int(temp_string.strip())
						except:
							pass
						auth_params[param] = fin_string
					else:
						raise SIP_Error("AUTH: No parameter's value received")
				print ("::FOR LOGGING PURPOSE. SIP_AUTH_FUNCTION. End of parsing::",auth_params)
				return auth_params
			else: 
				raise SIP_Error("AUTH: No auth parameters are received")


	def generate_value(self, variable):
		"""Generates and returns the requested value of a variable or None"""
		if variable in self._generators:
			return self._generators[variable]()

class SIP_Error(Exception):

    def __init__(self, description):
        self.description = description