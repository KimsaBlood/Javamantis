class Prioridades:
	def __init__(self,numero,expresion,nombre):
		self.numero=numero
		self.expresion=expresion
		self.nombre=nombre

	def setNumero(self,numero):
		self.numero=numero

	def setExpresion(self,expresion):
		self.expresion=expresion

	def setNombre(self,nombre):
		self.nombre=nombre

	def getNumero(self):
		return self.numero

	def getExpresion(self):
		return self.expresion

	def getNombre(self):
		return self.nombre