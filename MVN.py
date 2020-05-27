import memory
import register
import ULA
import device

def clean(line):
	res=[]
	line=line.split(" ")
	for word in line:
		if word!="":
			res.append(word)
	return res

class MVN:
	def __init__(self):
		self.mem=memory.memory()
		self.MAR=register.register()
		self.MDR=register.register()
		self.IC=register.register()
		self.IR=register.register()
		self.OP=register.register()
		self.OI=register.register()
		self.AC=register.register()
		self.ula=ULA.ULA()
		self.devs=[]
		self.devs.append(device.device(0,0))
		self.devs.append(device.device(1,0))

	def fetch(self):
		self.MAR.set_value(self.IC.get_value())
		self.get_mem(self.MAR.get_value())

	def decode(self):
		self.IR.set_value(self.MDR.get_value())
		self.OP.set_value(self.IR.get_value()//0x1000)
		self.OI.set_value(self.IR.get_value()-0x1000*self.OP.get_value())

	def execute(self):
		if self.OP.get_value()==0:
			return self.jp()
		elif self.OP.get_value() in [1,2]:
			if self.ula.execute(self.OP.get_value(), self.AC.get_value()):
				self.IC.set_value(self.OI.get_value())
			else:
				self.IC.set_value(self.IC.get_value()+2)
			return True
		elif self.OP.get_value()==3:
			return self.lv()
		elif self.OP.get_value() in [4,5,6,7]:
			self.get_mem(self.OI.get_value())
			self.AC.set_value(self.ula.execute(self.OP.get_value(), self.AC.get_value(), self.MDR.get_value()))
			self.IC.set_value(self.IC.get_value()+2)
			return True
		elif self.OP.get_value()==8:
			return self.ld()
		elif self.OP.get_value()==9:
			return self.mm()
		elif self.OP.get_value()==10:
			return self.sc()
		elif self.OP.get_value()==11:
			return self.rs()
		elif self.OP.get_value()==12:
			return self.hm()
		elif self.OP.get_value()==13:
			return self.gd()
		elif self.OP.get_value()==14:
			return self.pd()
		elif self.OP.get_value()==15:
			return self.os()

	def step(self):
		self.fetch()
		self.decode()
		return self.execute()

	def get_mem(self, addr):
		self.MDR.set_value(self.mem.get_value(addr))

	def jp(self):
		self.IC.set_value(self.OI.get_value())
		return True

	def lv(self):
		self.AC.set_value(self.OI.get_value())
		self.IC.set_value(self.IC.get_value()+2)
		return True

	def ld(self):
		self.get_mem(self.OI.get_value())
		self.AC.set_value(self.MDR.get_value())
		self.IC.set_value(self.IC.get_value()+2)
		return True

	def mm(self):
		self.mem.set_value(self.OI.get_value(), self.AC.get_value())
		self.IC.set_value(self.IC.get_value()+2)
		return True

	def sc(self):
		self.mem.set_value(self.OI.get_value(), self.AC.get_value()+2)
		self.IC.set_value(self.OI.get_value()+2)
		return True

	def rs(self):
		self.get_mem(self.OI.get_value())
		self.IC.set_value(self.MDR.get_value())
		return True

	def hm(self):
		return False

	def gd(self):
		for dev in self.devs:
			if self.OI.get_value()//0x0100==dev.get_type() and self.OI.get_value()%0x0100==dev.get_UC():
				self.AC.set_value(dev.get_data())
		self.IC.set_value(self.IC.get_value()+2)
		return True	

	def pd(self):
		for dev in self.devs:
			if self.OI.get_value()//0x0100==dev.get_type() and self.OI.get_value()%0x0100==dev.get_UC():
				dev.put_data(self.AC.get_value())
		self.IC.set_value(self.IC.get_value()+2)
		return True

	def os(self):
		print("Error number "+hex(self.AC.get_value()))
		self.IC.set_value(self.IC.get_value()+2)
		return True

	def print_state(self):
		return hex(self.MAR.get_value())[2:].zfill(4)+" "+hex(self.MDR.get_value())[2:].zfill(4)+" "+hex(self.IC.get_value())[2:].zfill(4)+" "+hex(self.IR.get_value())[2:].zfill(4)+" "+hex(self.OP.get_value())[2:].zfill(4)+" "+hex(self.OI.get_value())[2:].zfill(4)+" "+hex(self.AC.get_value())[2:].zfill(4)

	def set_memory(self, guide):
		for data in guide:
			self.mem.set_value(int(data[0], 16), int(data[1], 16))

	def dump_memory(self, start, stop):
		self.mem.show(start, stop)

	def create_disp(self):
		file=open("disp.lst", "r")
		lines=file.read().split("\n")
		for line in lines:
			line=clean(line)
			if line[0]=="0":
				if len(line)!=3 or line[2]!="mvn.dispositivo.Teclado":
					raise ValueError("'disp.lst' file badly formulated")
				self.devs.append(device.device(0, int(line[1])))
			elif line[0]=="1":
				if len(line)!=3 or line[2]!="mvn.dispositivo.Monitor":
					raise ValueError("'disp.lst' file badly formulated")
				self.devs.append(device.device(1, int(line[1])))
			elif line[0]=="2":
				if len(line)!=4 or line[2]!="mvn.dispositivo.Impressora":
					raise ValueError("'disp.lst' file badly formulated")
				self.devs.append(device.device(1, int(line[1]), printer=line[3]))
			elif line[0]=="3":
				if len(line)!=5 or line[2]!="mvn.dispositivo.Disco":
					raise ValueError("'disp.lst' file badly formulated")
				self.devs.append(device.device(1, int(line[1]), line[3], line[4]))

	def print_devs(self):
		translate={"0":"Teclado", "1":"Monitor", "2":"Impressora", "3":"Disco"}
		for dev in self.devs:
			print("  "+str(dev.get_type())+"    "+str(dev.get_UC()).zfill(2)+"   "+translate[str(dev.get_type())])

	def show_available_devs(self):
		self.devs[0].show_available()

	def new_dev(self, dtype, UC, file=None, rwb=None, printer=None):
		for dev in self.devs:
			if dev.get_type()==dtype and dev.get_UC()==UC:
				raise ValueError("Device ja existe")
		self.devs.append(device.device(dtype, UC, file, rwb, printer))

	def rm_dev(self, dtype, UC):
		for dev in range(len(self.devs)):
			if self.devs[dev].get_type()==dtype and self.devs[dev].get_UC()==UC:
				self.devs.pop(dev)