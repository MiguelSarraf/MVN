import address

MIN_ADDR=0x0000
MAX_ADDR=0x0FFF
MIN_VALUE=-0x0000
MAX_VALUE=0xFFFF

def valid_addr(addr):
	return (MIN_ADDR<=addr and addr<=MAX_ADDR)

def valid_value(num):
	if not(MIN_VALUE<=num and num<=MAX_VALUE):
		raise ValueError("Incompatible size")

class memory:
	def __init__(self, value=0x0000):
		valid_value(value)
		self.map=[]
		for cont in range(MAX_ADDR//2):
			self.map.append(address.address(2*cont, value//0x100))
			self.map.append(address.address(2*cont+1, value-(value//0x100)*0x100))

	def get_value(self, addr):
		valid_addr(addr)
		return self.map[addr].get_value()*0x100+self.map[addr+1].get_value()

	def set_value(self, addr, value):
		valid_addr(addr)
		valid_value(value)
		self.map[addr].set_value(value//0x100)
		self.map[addr+1].set_value(value-(value//0x100)*0x100)

	def show(self, start, stop):
		valid_addr(start)
		valid_addr(stop)
		if start>stop:
			raise ValueError("Uncompatible values")
		print("       00  01  02  03  04  05  06  07  08  09  0A  0B  0C  0D  0E  0F  ")
		print("-----------------------------------------------------------------------")
		line=hex(start//0x0010)[2:].zfill(3)+"0:  "+"    "*(start%0x0010)
		current_line=start//0x0010
		current_index=start-current_line*0x0010
		final_line=stop//0x0010
		final_index=stop-final_line*0x0010
		if current_line==final_line:
			while current_index<=final_index:
				line+=hex(self.map[current_line*0x0010+current_index].get_value())[2:].zfill(2)+"  "
				current_index+=1
			print(line)
		else:
			while current_line<final_line:
				while current_index<=0xF:
					line+=hex(self.map[current_line*0x0010+current_index].get_value())[2:].zfill(2)+"  "
					current_index+=1
				print(line)
				current_line+=1
				current_index=0
				line=hex(current_line)[2:].zfill(3)+"0:  "
			while current_index<=final_index:
				line+=hex(self.map[current_line*0x0010+current_index].get_value())[2:].zfill(2)+"  "
				current_index+=1
			print(line)