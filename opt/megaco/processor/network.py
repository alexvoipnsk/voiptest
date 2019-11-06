from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, IPPROTO_TCP
from socket import timeout as sock_timeout
from sys import exit
import sctp
import time

class NetworkAdapter:
	"""Class for data exchange over a network.
       Binds to a given node
	"""
	
	def __init__(self, from_node, *to_socks):
		self.buffer = from_node.network_buffer  # Network buffer size from the configuration file
		self.node_id = from_node.id             # The node to which the NetworkAdapter is binded
		self._socket = NetworkAdapter._configure_socket(from_node)  # Configured socket
		self._routes = NetworkAdapter._configure_routes(*to_socks)  # Routes to connected nodes (dictionary by the pattern "connection_id : connected_node")
		self._remote_addr = (None, None)
		self.transport = from_node.transport
		self.proto = from_node.proto
		#self.proto_type = from_node.proto_type

	@staticmethod
	def _configure_socket(node):
		"""Configures and returns an UDP socket by node properties
		If the error is caught, makes the error exit
		"""
		if node.transport == "udp":
			try:
				sock = socket(AF_INET, SOCK_DGRAM)
				sock.bind((node.ipaddr,node.port))
			except (OSError,IOError) as error:
				AppLogger.error("Creation socket error for Node '{id}': {error}'".format(id=node.id, error=error))
				exit(1)
		elif node.transport == "sctp":
			try:
				sock = sctp.sctpsocket_tcp(AF_INET)
				sock.bind((node.ipaddr,node.port))
			except (OSError,IOError) as error:
				AppLogger.error("Creation socket error for Node '{id}': {error}'".format(id=node.id, error=error))
				exit(1)
		elif node.transport == "tcp":
			try:
				sock = socket(AF_INET, IPPROTO_TCP)
				sock.bind((node.ipaddr,node.port))
			except (OSError,IOError) as error:
				AppLogger.error("Creation socket error for Node '{id}': {error}'".format(id=node.id, error=error))
				exit(1)
		else:
			AppLogger.error("Creation socket error for Node '{id}': {error}'".format(id=node.id, error="Invalid protocol"))
			exit(1)
		return sock

	@staticmethod
	def _configure_routes(*nodes):
		"""Configures and returns routes to connected nodes (dictionary by the pattern "connection_id : connected_node")"""
		return dict([(node.id, (node.ipaddr,node.port)) for node in nodes]) 

	def send(self, message, to_node):
		"""Sends a message to the remote node
		Returns the action result and its info
		"""
		try:
			self._socket.sendto(message.encode(), self._routes[to_node])
		except (OSError,IOError) as error:
			return (False, "Message has not been sent: %s" % str(error))
		return (True, "Message has been successfully sent to node '%s:%s'" % self._routes[to_node])

	def send_sctp(self, message, mes_type, to_node, used_ppid=0, used_stream=0):
		"""Sends a message to the remote node
		Returns the action result and its info
		"""
		try:
			if self._remote_addr != (None, None):
				self._socket.sctp_send(message, to=self._remote_addr, ppid=used_ppid, stream=used_stream)
			else:
				self._socket.sctp_send(message, to=self._routes[to_node], ppid=used_ppid, stream=used_stream)
		except (OSError,IOError) as error:
			return (False, "Message has not been sent: %s" % str(error))
		return (True, "Message '%s'" % mes_type + " has been successfully sent to node '%s:%s'" % self._routes[to_node])

	def send_tcp(self, message, to_node):
		"""Sends a message to the remote node
		Returns the action result and its info
		"""
		try:
			if self._remote_addr != None:
				self._socket.send(message, to=self._remote_addr)
			else:
				self._socket.send(message, to=self._routes[to_node])
		except (OSError,IOError) as error:
			return (False, "Message has not been sent: %s" % str(error))
		return (True, "Message has been successfully sent to node '%s:%s'" % self._routes[to_node])

	def recv(self, from_node, timeout, sec_from_node):
		"""Receives a message from the remote node by timeout
		Returns the action result, action log and received data
		"""
		self._socket.settimeout(timeout/1000)    # Setting a timeout for the receiving action
		try:
			data, node = self._socket.recvfrom(self.buffer)
		except (OSError, IOError, sock_timeout) as error:
			return (False, "Message has not been received: " + str(error), "NO_MESSAGE")
		else:
			print ("PP", node, self._remote_addr, sec_from_node)
			if node == None:
				return (False, "Message has not been received", None)
			if self._remote_addr != (None, None):
				return (True, "Message has been successfully received from node '%s:%i'" % self._remote_addr, data)
			if sec_from_node!=99999:
				if node == self._routes[from_node] or node == sec_from_node:  # The message must be received from the expected node
					pass
				else:
					return (False, "Message has been received from unexpeted node '%s:%i'" % node, None)
			else:
				if node != self._routes[from_node]:  # The message must be received from the expected node
					return (False, "Message has been received from unexpeted node '%s:%i'" % node, None)
		print (time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()), ":Node(for logging purpose) ", node)
		return (True, "Message has been successfully received from node '%s:%i'" % node, data)#.decode()) - moved to CATCH instruction

	def connect(self, to_node, mode):
		"""Connect to TCP or SCTP peer"""
		self._remote_addr = (None, None)
		try:
			if (mode == "server"):
				self._socket.listen()
				self._socket, self._remote_addr = self._socket.accept()
				return (True, "Listen socket has been successfully accepted from peer '%s:%i'" % self._remote_addr)
			else:
				self._socket.connect(self._routes[to_node])
				return (True, "Peer has been successfully connected to node '%s'" % to_node)
		except (OSError, IOError, sock_timeout) as error:
			return (False, "Peer has not been connected: " + str(error))

	def close(self):
		"""Closes the open socket"""
		self._socket.close()

	def __repr__(self):
		return "Network adapter for Node '%s'" % self.node_id