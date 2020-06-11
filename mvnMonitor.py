__author__="Miguel Sarraf Ferreira Santucci"
__email__="miguel.sarraf@usp.br"
__version__="5.0"

import MVN
import os.path

#Print all the commands available
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

'''Start an MVN, check if there is any 'disp.lst' file and 
inicialze the devices in it, return the MVN inicialized'''
def inicialize():
	mvn=MVN.MVN()
	print("MVN Inicializada\n")
	if os.path.exists("disp.lst"):
		mvn.create_disp()
		print("Dispositivos de 'disp.lst' inicializados")
	else:
		print("Inicializacao padrao de dispositivos\n")
	return mvn

#Print the header of the MVN
def head():
	print("                Escola Politécnica da Universidade de São Paulo")
	print("                 PCS3616 - Simulador da Máquina de von Neumann")
	print("          MVN versão 5.0 (Maio/2020) - Todos os direitos reservados")

#Print the header for the devices
def dev_head():
	print("Tipo   UC   Dispositivo")
	print("---------------------------------")

#Print the header for the registers
def reg_head():
	print(" MAR  MDR  IC   IR   OP   OI   AC")
	print("---- ---- ---- ---- ---- ---- ----")

'''Separate an given string by spaces and remove substrings with 
no content'''
def clean(line):
	res=[]
	line=line.split(" ")
	for word in line:
		if word!="":
			res.append(word)
	return res

'''Open given file, read it, separate memory and addresses and 
send them to the MVN memory'''
def load(name, mvn):
	file=open(name, "r")
	code=file.read().split("\n")
	line=0
	while line < len(code):
		try:
			code[line]=code[line][:code[line].index(";")]
		except:
			pass
		code[line]=clean(code[line])
		if len(code[line])!=2:
			if len(code[line])==0:
				code.pop(line)
				line-=1
			else:
				raise ValueError("Mais de dois numeros na instrucao")
		line+=1
	mvn.set_memory(code)
	print("Programa "+name+" carregado")

"""
Here starts the main code for the MVN's user interface, this will 
look like a cmd to the user, but operating the MVN class
"""

#First thing to be done is inicialize our MVN
mvn=inicialize()
#Show up the header for the MVN
head()
#Show options available
help()

'''These booleans will represent if the code should continue to 
execute (goon), if the register values are to be shown on screen 
(vals) and if MVN should be executed step by step (sbs)
'''
goon=False
vals=True
sbs=False

#This loop will deal with the MVN's interface commands
while True:
	command=input("\n> ")
	command=clean(command)

	#No action to be taken if nothing was typed
	if len(command)==0:
		pass

	#To reinicialize the MVN is just to inicialize it one more time
	elif command[0]=="i":
		mvn=inicialize()

	'''To load an program, one argument (the file) is required, if 
	it's not given, ask for it, if more are passed, cancel operation'''
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

	'''To run the program we have to ask the user it's preference 
	on the starting address and on vals and sbs booleans, so one by 
	one, those are asked, note that if vals is false, sbs must be 
	false too.
	Got these values, execute instructions until goon turns False.'''
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
				reg_head()

			while goon:
				goon=mvn.step()
				if vals:
					if sbs:
						read=input(mvn.print_state())
					else:
						print(mvn.print_state())
					
		else:
			print("Nenhum arquivo foi carregado, nada a ser executado.")

	#Start the debugger mode
	elif command[0]=="b":
		pass

	#Display the available devices and give options to add or remove
	elif command[0]=="s":
		dev_head()
		mvn.print_devs()
		choice=input("Adicionar(a) ou remover(r) (ENTER para cancelar): ")
		if choice=="a":
			mvn.show_available_devs()
			dtype=input("Entrar com o tipo de dispositivo (ou ENTER para cancelar): ")
			try:
				dtype=int(dtype)
				go=True
			except:
				print("O tipo de dispositivo especificado é inválido (especifique um valor numérico).")
				go=False
			if go:
				UC=input("Entrar com a unidade logica (ou ENTER para cancelar): ")
				try:
					UC=int(UC)
					go=True
				except:
					print("O tipo de dispositivo especificado é inválido (especifique um valor numérico).")
					go=False
			if go:
				if dtype==2:
					name=input("Entrar com o nome da impressora: ")
					mvn.new_dev(dtype, UC, printer=name)
				elif dtype==3:
					file=input("Digite o nome do arquivo: ")
					met=input("Digite o modo de operação -> Leitura(l), Escrita(e) ou Leitura e Escrita(b): ")
					mvn.new_dev(dtype, UC, file, met)
				else:
					mvn.new_dev(dtype, UC)
				print("Dispositivo adicionado (Tipo: "+str(dtype)+" - unidade logica: "+str(UC)+")")
		elif choice=="r":
			mvn.show_available_devs()
			dtype=input("Entrar com o tipo de dispositivo (ou ENTER para cancelar): ")
			try:
				dtype=int(dtype)
				go=True
			except:
				print("O tipo de dispositivo especificado é inválido (especifique um valor numérico).")
				go=False
			if go:
				UC=input("Entrar com a unidade logica (ou ENTER para cancelar): ")
				try:
					UC=int(UC)
					go=True
				except:
					print("O tipo de dispositivo especificado é inválido (especifique um valor numérico).")
					go=False
			if go:
				mvn.rm_dev(dtype, UC)

	#Display actual state os the MVN registers
	elif command[0]=="g":
		reg_head()
		print(mvn.print_state())

	#Display the memmory of the MVN given the start and end addresses
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

	#Display the available commands
	elif command[0]=="h":
		help()
		
	#Exit terminal
	elif command[0]=="x":
		print("Terminal encerrado.")
		exit()