import MVN
import os.path

def help():
	print(" COMANDO  PARÂMETROS           OPERAÇÃO")
	print("---------------------------------------------------------------------------")
	print("    i                          Re-inicializa MVN")
	print("    p     [arq]                Carrega programa para a memória")
	print("    r     [addr] [regs]        Executa programa")
	print("    b                          Ativa/Desativa modo Debug")
	print("    s                          Manipula dispositivos de I/O")
	print("    g                          Lista conteúdo dos registradores")
	print("    m     [ini] [fim] [arq]    Lista conteúdo da memória")
	print("    h                          Ajuda")
	print("    x                          Finaliza MVN e terminal")

def inicialize():
	mvn=MVN.MVN()
	print("MVN Inicializada\n")

	if os.path.exists("disp.lst"):
		#mvn.create_disp()
		pass
	else:
		print("Inicializacao padrao de dispositivos\n")
	return mvn

def head():
	print("                Escola Politécnica da Universidade de São Paulo")
	print("                 PCS3616 - Simulador da Máquina de von Neumann")
	print("          MVN versão 5.0 (Maio/2020) - Todos os direitos reservados")

def clean(line):
	res=[]
	line=line.split(" ")
	for word in line:
		if word!="":
			res.append(word)
	return res

def load(name, mvn):
	file=open(name, "r")
	code=file.read().split("\n")
	for line in range(len(code)):
		try:
			code[line]=code[line][:code[line].index(";")]
		except:
			pass
		code[line]=clean(code[line])
		if len(code[line])!=2:
			if len(code[line])==0:
				code.pop(line)
			else:
				raise ValueError("Mais de dois numeros na instrucao")
	mvn.set_memory(code)
	print("Programa "+name+" carregado")

mvn=inicialize()
head()
help()

goon=False
vals=True
sbs=True

while True:
	command=input("\n> ")
	command=clean(command)
	if command[0]=="i":
		mvn=inicialize()
	elif command[0]=="p":
		if len(command)==1:
			name=input("Informe o nome do arquivo de entrada: ")
			name=clean(name)
			if len(name)!=1:
				print("Arquivo deve ter exatamente 1 palavra, "+str(len(command))+" passadas.")
			else:
				load(name[0], mvn)
				goon=True
				pass
		elif len(command)>2:
			print("Arquivo deve ter exatamente 1 palavra, "+str(len(command)-1)+" passadas.")
		else:
			name=command[1]
			load(name, mvn)
			goon=True
	elif command[0]=="r":
		if goon:
			try:
				mvn.IC.set_value(int(input("Informe o endereco do IC ["+str(mvn.IC.get_value()).zfill(4)+"]: "), 16))
			except:
				pass

			if vals:
				s="s"
			else:
				s="n"
			try:
				vals=input("Exibir valores dos registradores a cada passo do ciclo FDE? <s/n> ["+s+"]: ")
				vals=vals=="s" or len(vals)==0
			except:
				vals=True

			if vals:
				if sbs:
					s="s"
				else:
					s="n"
				try:
					sbs=input("Excutar a MVN passo a passo? <s/n> ["+s+"]: ")
					sbs=sbs=="s" or len(sbs)==0
				except:
					sbs=True
			else:
				sbs=False

			if vals:
				print(" MAR  MDR  IC   IR   OP   OI   AC")
				print("---- ---- ---- ---- ---- ---- ----")

			while goon:
				goon=mvn.step()
				if vals:
					if sbs:
						read=input(mvn.print_state())
					else:
						mvn.print_state()
					
		else:
			print("Nenhum arquivo foi carregado, nada a ser executado.")
	elif command[0]=="b":
		pass
	elif command[0]=="s":
		pass
	elif command[0]=="g":
		pass
	elif command[0]=="m":
		if len(command)!=3:
			try:
				start=int(input("Informe o endereco inicial: "), 16)
				stop=int(input("Informe o endereco final: "), 16)
				mvn.dump_memory(start, stop)
			except:
				print("Enderecos não são valores hexadecimais.")
		else:
			try:
				start=int(command[1], 16)
				stop=int(command[2], 16)
				mvn.dump_memory(start, stop)
			except:
				print("Enderecos não são valores hexadecimais.")
	elif command[0]=="h":
		help()
	elif command[0]=="x":
		print("Terminal encerrado.")
		exit()