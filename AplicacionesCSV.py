from opcionesCSV import opcionesCSV
class AplicacionesCSV:
	def __init__(self,nombre=None,opcs=None,info=None):
		self.nombre=nombre
		self.opciones=opcs

	def setNombre(self,nombre):
		self.nombre=nombre

	def getNombre(self):
		return self.nombre

	def setOpciones(self,opciones):
		self.opciones=opciones

	def getOpciones(self):
		return self.opciones