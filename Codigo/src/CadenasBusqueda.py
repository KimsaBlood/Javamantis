from Extracciones import Extracciones
class CadenasBusqueda:
	""""""
	def __init__(self,nombre,cadena,expresion,extracciones):
		self.nombre=nombre
		self.cadena=cadena
		self.expresion=expresion
		self.extracciones=[]
		for l in extracciones:
			self.extracciones.append(Extracciones(extracciones["nombre"],extracciones["expresiones"]))

	def setExtracciones(self,extracciones):
		self.extraciones=extracciones

	def setNombre(self,nombre):
		self.nombre=nombre

	def setCadena(self,cadena):
		self.cadena=cadena

	def setExpresion(self,expresion):
		self.expresion=expresion

	def getExtracciones(self):
		return self.extracciones

	def getNombre(self):
		return self.nombre

	def getCadena(self):
		return self.cadena

	def getExpresion(self):
		return self.expresion