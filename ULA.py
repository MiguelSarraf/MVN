MIN_VALUE=0x0000
MAX_VALUE=0xFFFF

#Test if argument is 1,2,4,5,6 or 7, raise error
def is_valid_instru(num):
	if num not in [1,2,4,5,6,7]:
		raise ValueError("Incompatible instruction")

#Test if argument is between 0x0000 and 0xFFFF, raise error
def valid_value(num):
	if not(MIN_VALUE<=num and num<=MAX_VALUE):
		raise ValueError("Incompatible size")


'''
This class represents an simple Logic and Arthimatic Unit 
(LAU), here called by ULA (in portuguese), this LAU can only
operate equal zero, less than zero, addition, subtraction, 
multiplication and division mapped in the operations 1,2,4,5,6,7
respectively.
It contains methods for all of these operations and one method 
to call the others.
'''
class ULA:
	#Inicialize the LAU
	def __init__(self):
		pass

	'''Check if the given instruction is valid and performs the
	right operation'''
	def execute(self, op, ac, oi=0x0000):
		is_valid_instru(op)
		valid_value(ac)
		valid_value(oi)
		if op==1:
			return self.is_zero(ac)
		elif op==2:
			return self.is_neg(ac)
		elif op==4:
			return self.add(ac, oi)
		elif op==5:
			return self.sub(ac, oi)
		elif op==6:
			return self.mul(ac, oi)
		elif op==7:
			return self.div(ac, oi)
	
	def is_zero(self, num):
		return num==0x0000

	def is_neg(self, num):
		return num>=0x8000

	def add(self, num1, num2):
		return (num1+num2)%(1<<16)

	def sub(self, num1, num2):
		return (num1-num2)%(1<<16)

	def mul(self, num1, num2):
		return (num1*num2)%(1<<16)

	def div(self, num1, num2):
		signal=False
		if self.is_neg(num1):
			num1=self.mul(num1, 0xFFFF)
			signal=not signal
		if self.is_neg(num2):
			num2=self.mul(num2, 0xFFFF)
			signal=not signal
		if signal:
			return self.mul(num1//num2, 0xFFFF)
		return num1//num2