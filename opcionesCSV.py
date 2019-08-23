class opcionesCSV:
	def __init__(self,info,nombre):
		self.info=info
		self.nombre=nombre

	def setInfo(self,info):
		self.info=info

	def getInfo(self):
		return self.info

	def getNombre(self):
		return self.nombre

	def setNombre(self):
		self.nombre=nombre

	def toDict(self):
		return {self.getNombre():self.getInfo()}