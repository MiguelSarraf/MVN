import sys
import os.path

'''Separate an given string by spaces and remove substrings with 
no content'''
def clean(line):
	res=[]
	line=line.split(" ")
	for word in line:
		if word!="":
			res.append(word)
	return res

#Test if the given file exists, raise error
def valid_file(file):
	if not(os.path.exists(file)):
		raise ValueError("File does not exist")

'''Open given file, read it, clean tabs and separate by enters
(this is the raw descriptor), then remove comments and null lines
(this is the code descriptor), return both descriptors cleaned'''
def load(name):
	valid_file(name)
	file=open(name, "r")
	char=0
	raw=file.read()
	code=""
	raw_mod=""
	while char<len(raw):
		if raw[char]=="\t":
			raw_mod+=" "
		else:
			raw_mod+=raw[char]
		char+=1
	raw_mod=raw_mod.split("\n")
	code=raw_mod[:]
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
		line+=1
	line=0
	while line<len(raw_mod):
		raw_mod[line]=clean(raw_mod[line])
		line+=1
	return raw_mod, code

#Number format dictionary
num_format={"/":16, 
			"'":"ASCII", 
			"=":10, 
			"@":8, 
			"#":2}

'''Receives an list of two strings as [<type of int>,<int>] and
returns the correspondent integer to the type passed'''
def get_number(num):
	if num_format[num[0]]=="ASCII":
		return ord(num[1:])
	else:
		return int(num[1:], num_format[num[0]])

#Operation dictionary
mnem_op={"K": 0x0,
		"JP":0x0,
		"JZ":0x1, 
		"JN":0x2, 
		"LV":0x3, 
		"AD":0x4, 
		"SB":0x5, 
		"ML":0x6, 
		"DV":0x7, 
		"LD":0x8, 
		"MM":0x9, 
		"SC":0xA, 
		"RS":0xB, 
		"HM":0xC, 
		"GD":0xD, 
		"PD":0xE, 
		"OS":0xF}

file=sys.argv[1]
raw, code=load(file)

#Save entry_points and externals
entry_points={}
externals={}
ext_count=0
for line in code:
	if line[1]==">":
		entry_points[line[0]]=None
	elif line[1]=="<":
		externals[line[0]]=ext_count
		ext_count+=1
	else:
		pass

#Define rotules and complete entry_points
rotules={}
rotules_reloc={}
relocable=True
addr=0
for line in code:
	if len(line)==2:
		if line[0] in ["@", "&"]:
			relocable=line[0]=="&"
			addr=get_number(line[1])
		elif line[1] in [">", "<"]:
			pass
		elif line[0]=="$":
			addr+=2*get_number(line[1])-2
		else:
			addr+=2
	else:
		rotules[line[0]]=addr
		rotules_reloc[line[0]]=relocable
		if line[0] in entry_points:
			entry_points[line[0]]=addr
		elif line[1]=="$":
			addr+=2*get_number(line[2])
		elif line[1] in ["@", "&"]:
			relocable=line[1]=="&"
			addr=get_number(line[2])
		else:
			addr+=2

#Insert entry_points and externals in final code
final=[]
for ext in externals:
	final.append([0x4000+externals[ext], 0x0000, True])
for ep in entry_points:
	final.append([rotules_reloc[ep]*0x2000+entry_points[ep], 0x0000, True])

#Pass through the code defining addresses and translating
'''First nibble of the address has the following composition:
[addr relocability][o resolution][op relocability][op location]
  0=abs   1=reloc ||0=res 1=nres||0=abs  1=reloc ||0=in  1=out'''
addr=0
relocable=True
end=False
line_n=0
for line in code:
	if len(line)==2:
		#symbols for defining relocability
		if line[0] in ["@", "&"]:
			relocable=line[0]=="&"
			addr=get_number(line[1])-2
		#symbol for defining constants
		elif line[0]=="K":
			final.append([8*relocable*0x1000+addr, get_number(line[1]), False])
		#symbol for reserving space
		elif line[0]=="$":
			n=get_number(line[1])
			for i in range(n):
				final.append([8*relocable*0x1000+addr, 0, False])
				addr+=2
			new_raw=raw[:line_n+2]
			new_raw.extend([[0]]*(n-1))
			new_raw.extend(raw[line_n+2:])
			raw=new_raw
			line_n+=n-1
			addr-=2
		#symbol for ending code
		elif line[0]=="#":
			end=True
			break
		#symbols for instructions
		elif line[0] in mnem_op:
			if line[1] in externals:
				final.append([(8*relocable+5)*0x1000+addr, mnem_op[line[0]]*0x1000+externals[line[1]], False])
			elif line[1] in rotules:
				final.append([(8*relocable+2*rotules_reloc[line[1]])*0x1000+addr, mnem_op[line[0]]*0x1000+rotules[line[1]], False])
			else:
				final.append([10*relocable*0x1000+addr, mnem_op[line[0]]*0x1000+get_number(line[1]), False])
		addr+=2
	else:
		#symbols for defining relocability
		if line[1] in ["@", "&"]:
			relocable=line[1]=="&"
			addr=get_number(line[2])-2
		#symbol for defining constants
		elif line[2]=="K":
			final.append([8*relocable*0x1000+addr, get_number(line[2]), False])
		#symbol for reserving space
		elif line[1]=="$":
			n=get_number(line[2])
			for i in range(n):
				final.append([8*relocable*0x1000+addr, 0, False])
				addr+=2
			new_raw=raw[:line_n+2]
			new_raw.extend([[0]]*(n-1))
			new_raw.extend(raw[line_n+2:])
			raw=new_raw
			line_n+=n-1
			addr-=2
		#symbol for ending code
		elif line[1]=="#":
			end=True
			break
		#symbols for instructions
		elif line[1] in mnem_op:
			if line[2] in externals:
				final.append([(8*relocable+5)*0x1000+addr, mnem_op[line[1]]*0x1000+externals[line[2]], False])
			elif line[2] in rotules:
				final.append([(8*relocable+2*rotules_reloc[line[2]])*0x1000+addr, mnem_op[line[1]]*0x1000+rotules[line[2]], False])
			else:
				final.append([10*relocable*0x1000+addr, mnem_op[line[1]]*0x1000+get_number(line[2]), False])
		addr+=2
	line_n+=1

#Erase line with relocability data from code
line=0
while line < len(code):
	if len(code[line])>1:
		if code[line][0] in ["@", "&"] or code[line][1] in ["@", "&"]:
			code.pop(line)
			line-=1
	line+=1

#Write in output mvn file
mvn_file=open(file[:file.index(".")]+".mvn", "w")
for line in final:
	if line[2]:
		mvn_file.write(hex(line[0])[2:].zfill(4)+" "+hex(line[1])[2:].zfill(4)+" ; '"+code[final.index(line)][0]+" "+code[final.index(line)][1]+"'\n")
	else:
		mvn_file.write(hex(line[0])[2:].zfill(4)+" "+hex(line[1])[2:].zfill(4)+"\n")
mvn_file.close()

#Write in the output lst file
lst_file=open(file[:file.index(".")]+".lst", "w")
line_code=0
line_final=0
for line in range(len(raw)):
	exit=""
	if raw[line][0]==code[line_code][0] or raw[line][0]==0:
		exit=hex(final[line_final][0])[2:].zfill(4)+" "+hex(final[line_final][1])[2:].zfill(4)+" ; "
		for word in raw[line]:
			if word!=0: exit+=word+" "
		if word!=0: line_code+=1
		line_final+=1
	else:
		exit+=";"
		for word in raw[line]:
			exit+=word+" "
	lst_file.write(exit+"\n")
lst_file.close()

print("Arquivo "+file+" montado para "+file[:file.index(".")]+".mvn"+" com sucesso!")