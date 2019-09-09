class Calculadora:
	def _init_(self):
		self.a=0
		self.b=0

	def suma(self,a,b):
		return a+b

	def resta(self,a,b):
		return a-b

obj=Calculadora()
print(obj.suma(1,3))