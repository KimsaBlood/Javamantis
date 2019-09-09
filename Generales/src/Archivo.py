import codecs
class Archivo():
	def __init__(self,nombre):
		self.nombre=nombre

	def setNombre(self,nombre):
		self.nombre=nombre

	def setContenido(self,contenido):
		self.contenido=contenido

	def getNombre(self):
		return self.nombre

	def leer(self):
		lines2=[]
		days_file = codecs.open(self.nombre,'r',encoding = "ISO-8859-1")
		lines=days_file.read().splitlines()
		self.contenido=lines
		return lines