class JNDI:
	def __init__(self,nombre,cadena,tipo,binario):
		self.nombre=nombre
		self.cadena=cadena
		self.tipo=tipo
		self.encontrado=0
		self.binario=binario

	def setBinario(self):
		self.binario=binario

	def getBinario(self):
		return self.binario

	def setTipo(self,tipo):
		self.tipo=tipo

	def getTipo(self):
		return self.tipo

	def setNombre(self,nombre):
		self.nombre=nombre

	def getNombre(self):
		return self.nombre

	def setCadena(self,cadena):
		self.cadena=cadena

	def getCadena(self):
		return self.cadena

	def getEncontrado(self):
		return self.encontrado

	def setEncontrado(self,encontrado):
		self.encontrado=encontrado

	def toDict(self):
		return {"Nombre":self.getNombre(),"Tipo":self.getTipo(),"Binario":self.getBinario()}