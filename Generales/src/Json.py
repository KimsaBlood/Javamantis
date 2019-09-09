import os
import json
class Json:

	def __init__(self,nombre,contenido=None):
		self.nombre=nombre
		self.contenido=contenido

	@classmethod
	def contenido(cls,nombre, contenido):
		return cls(nombre=nombre, contenido=contenido)

	def setNombre(nombre):
		self.nombre=nombre

	def getNombre(self):
		return nombre

	def convertirAJson(self):
		twitterDataFile = open(self.nombre, "w")
		twitterDataFile.write(json.dumps(self.contenido, indent=4, sort_keys=True))
		twitterDataFile.close()

	def leer(self):
		if os.path.isfile(self.nombre):
			with open(self.nombre,'r') as f:
				self.contenido=json.load(f)
		else:
			print("No existe el archivo")
		return self.contenido

	def setContenido():
		self.contenido=contenido

	def getContenido():
		return self.contenido