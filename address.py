MIN_VALUE=0x0000
MAX_VALUE=0x00FF

#Test if argument is between 0x0000 and 0x00FF, raise error
def valid_value(num):
	if not(MIN_VALUE<=num and num<=MAX_VALUE):
		raise ValueError("Incompatible size")

'''
This class is for an address in the memory, it is defined by
one address number and one value contained in this address.
It also contains to get address and value and to set the value
'''
class address:

	#Inicialize address and value
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