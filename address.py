MIN_VALUE=0x00
MAX_VALUE=0xFF

def valid_value(num):
	if not(MIN_VALUE<=num and num<=MAX_VALUE):
		raise ValueError("Incompatible size")

class address:
	def __init__(self, addr, value=0x00):
		valid_value(value)
		self.addr=addr
		self.value=value

	def set_value(self, value):
		valid_value(value)
		self.value=value

	def get_addr(self):
		return self.addr

	def get_value(self):
		return self.value