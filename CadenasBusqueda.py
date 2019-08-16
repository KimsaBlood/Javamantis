class CadenasBusqueda:
	""""""
	def __init__(self,nombre,cadena,expresion):
		self.nombre=nombre
		self.cadena=cadena
		self.expresion=expresion

	def setNombre(self,nombre):
		self.nombre=nombre

	def setCadena(self,cadena):
		self.cadena=cadena

	def setExpresion(self,expresion):
		self.expresion=expresion

	def getNombre(self):
		return self.nombre

	def getCadena(self):
		return self.cadena

	def getExpresion(self):
		return self.expresion