from random import randint
from time import strftime
from hashlib import md5

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

	def generate_value(self, variable):
		"""Generates and returns the requested value of a variable or None"""
		if variable in self._generators:
			return self._generators[variable]()

class Auth:
	"""Class for implementing of authentication"""

	@staticmethod
	def _digest_auth(auth_data):
		print ('8888', auth_data)
		if auth_data["authtype"]=="Digest":
			if auth_data["algorithm"]=="MD5":
				A1md5 = md5("{}:{}:{}".format(str(auth_data["authname"]), str(auth_data["realm"]), str(auth_data["password"])).encode('utf-8')).hexdigest()
				if "qop" in auth_data:
					if auth_data["qop"]=="auth":
						A2md5.update((auth_data["method"] + ":" + str(auth_data["digest-uri-value"])).encode())
					elif auth_data["qop"]=="auth-int":
						raise SIP_Error("AUTH: qop=auth-int isn't supported now")
						#A2 = method ":" digest_uri_value ":" H(entity-body)
					request_digest  = '"' + digest_value.update((A1md5 + ":" + str(auth_data["nonce"]) + ":" + str(auth_data["nc-value"])
            	                             + ":" + str(auth_data["cnonce-value"]) + ":" + auth_data["qop"] + ":" + A2md5).encode()) + '"'
				else:
					A2md5 = md5("{}:{}".format(str(auth_data["method"]), str(auth_data["digest-uri-value"])).encode('utf-8')).hexdigest()
					digest_value = md5("{}:{}:{}".format(A1md5, str(auth_data["nonce"]), A2md5).encode())
					request_digest  = digest_value.hexdigest()
					authorization='Authorization: Digest username="' + str(auth_data["authname"]) + '", realm="' + str(auth_data["realm"]) + '", nonce="' +str(auth_data["nonce"]) + '", uri="'+ str(auth_data["digest-uri-value"]) + '", response=' + request_digest + ', algorithm="' + str(auth_data["algorithm"])
			elif auth_data["algorithm"]=="MD5-sess":
				raise SIP_Error("AUTH: Only MD5 alorithm is supported")
				#A1 = H( unq(username-value) ":" unq(realm-value) + ":" + passwd ) + ":" + unq(nonce) + ":" + unq(cnonce-value)
			else:
				raise SIP_Error("AUTH: Only MD5 or MD5-sess alorithms are supported")
			return authorization
		else:
			raise SIP_Error("AUTH: Only Digest authentication is supported")


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
						temp_string = ''
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


class SIP_Error(Exception):

    def __init__(self, description):
        self.description = description