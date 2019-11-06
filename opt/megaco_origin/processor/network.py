from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from socket import timeout as sock_timeout
from sys import exit

class NetworkAdapter:
	"""Class for data exchange over a network.
       Binds to a given node
	"""
	
	def __init__(self, from_node, *to_nodes):
		self.buffer = from_node.network_buffer  # Network buffer size from the configuration file
		self.node_id = from_node.id             # The node to which the NetworkAdapter is binded
		self._socket = NetworkAdapter._configure_socket(from_node)  # Configured UDP socket
		self._routes = NetworkAdapter._configure_routes(*to_nodes)  # Routes to connected nodes (dictionary by the pattern "connection_id : connected_node")

	@staticmethod
	def _configure_socket(node):
		"""Configures and returns an UDP socket by node properties
		If the error is caught, makes the error exit
		"""
		try:
			sock = socket(AF_INET, SOCK_DGRAM)
			sock.bind((node.ip_address,node.port))
		except (OSError,IOError) as error:
			AppLogger.error("Creation socket error for Node '{id}': {error}'".format(id=node.id, error=error))
			exit(1)
		return sock

	@staticmethod
	def _configure_routes(*nodes):
		"""Configures and returns routes to connected nodes (dictionary by the pattern "connection_id : connected_node")"""
		return dict([(node.id, (node.ip_address,node.port)) for node in nodes]) 

	def send(self, message, to_node):
		"""Sends a message to the remote node

		Returns the action result and its info
		"""
		try:
			self._socket.sendto(message.encode(), self._routes[to_node])
		except (OSError,IOError) as error:
			return (False, "Message has not been sent: %s" % str(error))
		return (True, "Message has been successfully sent to node '%s:%s'" % self._routes[to_node])

	def recv(self, from_node, timeout):
		"""Receives a message from the remote node by timeout

		Returns the action result, action log and received data
		"""
		self._socket.settimeout(timeout/1000)    # Setting a timeout for the receiving action
		try:
			data, node = self._socket.recvfrom(self.buffer)
		except (OSError, IOError, sock_timeout) as error:
			return (False, "Message has not been received: " + str(error), None)
		else:
			if node != self._routes[from_node]:  # The message must be received from the expected node
				return (False, "Message has been received from unexpeted node '%s:%s'" % node, None)
		return (True, "Message has been successfully received from node '%s:%s'" % node, data.decode())

	def close(self):
		"""Closes the open socket"""
		self._socket.close()

	def __repr__(self):
		return "Network adapter for Node '%s'" % self.node_id