MIN_VALUE=-0x0000
MAX_VALUE=0xFFFF

def valid_value(num):
	if not(MIN_VALUE<=num and num<=MAX_VALUE):
		raise ValueError("Incompatible size")

class register:
	def __init__(self, value=0x00):
		valid_value(value)
		self.value=value

	def set_value(self, value):
		valid_value(value)
		self.value=value
		
	def get_value(self):
		return self.value