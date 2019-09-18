class Entornos:
	def __init__(self,nombre=None,carpeta=None):
		self.nombre=nombre
		self.carpeta=carpeta

	def setNombre(self,nombre):
		self.nombre=nombre

	def setCarpeta(self,carpeta):
		self.carpeta=carpeta

	def getNombre(self):
		return self.nombre

	def getCarpeta(self):
		return self.carpeta