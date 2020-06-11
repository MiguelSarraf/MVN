import os.path
import subprocess

MIN_VALUE=0x0000
MAX_VALUE=0xFFFF

#Test if argument is between 0 and 4, raise error
def is_valid_type(val):
	if not(val>=0 and val<=3):
		raise ValueError("Incompatible type")

#Test if the given file exists, raise error
def is_valid_file(file):
	if not(os.path.exists(file)):
		raise ValueError("File does not exist")

#Test if given rwb is valid, raise error
def is_valid_rwb(rwb):
	if rwb not in ["e", "l", "b"]:
		raise ValueError("Incompatible parameter")

#Test if the printer exists in OS, raise error
def is_valid_printer(printer):
	try:
		out=subprocess.check_output(["lpstat", "-p", printer])
	except:
		raise ValueError("Impressora invalida")

#Test if argument is between 0x0000 and 0xFFFF, raise error
def is_valid_value(num):
	if not(MIN_VALUE<=num and num<=MAX_VALUE):
		raise ValueError("Incompatible size")

'''
This class represents an simple I/O device for MVN, it can
hold monitor (output), keyboard (input), printer (output) 
or file (input and/or output).
It contains methods to return weather the device is readable
or writable, to input and output data, to get device type and 
UC, to print the possible devices and to terminate it.
'''
class device:

	'''Inicialize the device given the type, the UC and other
	convinient parameters'''
	def __init__(self, dtype, UC, file=None, rwb=None, printer=None):
		is_valid_type(dtype)
		self.dtype=dtype
		self.UC=UC
		if self.dtype==3:
			is_valid_rwb(rwb)
			if rwb=="e":
				self.file_write=open(file, "wb")
				self.file_read=None
			elif rwb=="l":
				is_valid_file(file)
				self.file_write=None
				self.file_read=open(file, "rb")
				self.buffer=self.file_read.read()
				self.counter=0
			elif rwb=="b":
				is_valid_file(file)
				self.file_write=open(file, "wb")
				self.file_read=open(file, "rb")
				self.buffer=self.file_read.read()
				self.counter=0
				self.file_write.write(bytes(self.buffer, "UTF-8"))
		elif self.dtype==2:
			is_valid_printer(printer)
			self.printer=printer
		elif self.dtype==0:
			self.buffer=[]

	#Return True weather the device is readable
	def is_readable(self):
		return self.dtype==0 or (self.dtype==3 and self.file_read!=None)

	#Return True weather the device is writable
	def is_writable(self):
		return self.dtype==1 or self.dtype==2 or self.dtype==3 and self.file_write!=None

	'''Get data from the device and return it, the limit to be 
	returned is one byte (or two nibbles)'''
	def get_data(self):
		if not self.is_readable():
			raise ValueError("Unreadable device")
		if self.dtype==0:
			if len(self.buffer)<2:
				read=input()
				for nibble in read:
					self.buffer.append(ord(nibble))
				self.buffer.append(ord("\n"))
			return self.buffer.pop(0)*0x0100+self.buffer.pop(0)
		elif self.dtype==3:
			if self.counter+2>len(self.buffer):
				print("No more data to get, returning 0x0000")
				return 0x0000
			else:
				self.counter+=2
				return self.buffer[self.counter-2]*0x0100+self.buffer[self.counter-1]

	'''Put given data to the device, the limit to be put is one
	byte (or two nibbles)'''
	def put_data(self, value):
		if not self.is_writable():
			raise ValueError("Unwritable device")
		is_valid_value(value)
		if self.dtype==1:
			print(chr(value//0x0100)+chr(value%0x0100))
		elif self.dtype==2:
			out=open("will_print.txt", "rb")
			out.write(value//0x0100)
			out.write(value%0x0100)
			subprocess.run("lpr -P "+self.printer+" will_print.txt")
			subprocess.run("rm will_print.txt")
		elif self.dtype==3:
			self.file_write.write(bytes(chr(value//0x0100), "UTF-8"))
			self.file_write.write(bytes(chr(value%0x0100), "UTF-8"))

	#Ends up the device
	def terminate(self):
		if self.dtype==3:
			try:
				self.file_write.close()
			except:
				pass

			try:
				self.file_read.close()
			except:
				pass

	#Return device type
	def get_type(self):
		return self.dtype

	#Return device UC
	def get_UC(self):
		return self.UC

	#Print the possible devices
	def show_available(self):
		print("Tipos de dispositivos disponíveis:")
		print("   Teclado    -> 0")
		print("   Monitor    -> 1")
		print("   Impressora -> 2")
		print("   Disco      -> 3")