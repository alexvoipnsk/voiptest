from time import strftime

class AppLogger:
	"""Class for application logging"""

	@staticmethod
	def info(log):
		"""Prints the log string in the INFO wrapper"""
		print(strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\033[92m INFO \033[0m" + log)

	@staticmethod
	def warning(log):
		"""Prints the log string in the WARNING wrapper"""
		print(strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\033[93m WARNING \033[0m" + log)

	@staticmethod
	def error(log):
		"""Prints the log string in the ERROR wrapper"""
		print(strftime("(%d.%m.%Y) %Hh:%Mm:%Ss") + "\033[1;31m ERROR \033[1;m" + log)