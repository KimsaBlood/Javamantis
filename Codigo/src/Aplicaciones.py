"""Clase aplicaciones definida por el arhivo de configuracion"""
class Aplicaciones:

	def __init__(self,nombre,ruta,carpetas):
		#Asignamos nombre del tipo string, ruta del tipo string y carpets del tipo list
		self.nombre=nombre
		self.ruta=ruta
		self.carpetas=carpetas

	#Getters y setters
	def getCarpetas(self):
		return self.carpetas

	def getNombre(self):
		return self.nombre

	def getRuta(self):
		return self.ruta

	def setNombre(self,nombre):
		self.nombre=nombre

	def setRuta(self,ruta):
		self.ruta=ruta

	def setCarpetas(self,carpetas):
		self.carpetas=carpetas