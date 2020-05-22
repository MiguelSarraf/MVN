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
	print("")

def inicialize():
	mvn=MVN.MVN()
	print("MVN Inicializada\n")

	if os.path.exists("disp.lst"):
		#mvn.create_disp()
		pass
	else:
		print("Inicializacao padrao de dispositivos\n")

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

inicialize()
head()
help()

goon=True
while goon:
	command=input("> ")
	command=clean(command)
	if command[0]=="i":
		inicialize()
	elif command[0]=="p":
		if len(command)==1:
			name=input("Informe o nome do arquivo de entrada: ")
			name=clean(name)
			if len(name)!=1:
				print("Arquivo deve ter exatamente 1 palavra, "+str(len(command))+" passadas.")
			else:
				#load(name)
				pass
		elif len(command)>2:
			print("Arquivo deve ter exatamente 1 palavra, "+str(len(command)-1)+" passadas.")
		else:
			name=command[1]
			#load(name)
	elif command[0]=="r":
		pass
	elif command[0]=="b":
		pass
	elif command[0]=="s":
		pass
	elif command[0]=="g":
		pass
	elif command[0]=="m":
		pass
	elif command[0]=="h":
		pass
	elif command[0]=="x":
		exit()