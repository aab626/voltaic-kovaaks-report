class NoStatFoundException(Exception):
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return self.msg

class LastNError(Exception):
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return self.msg
