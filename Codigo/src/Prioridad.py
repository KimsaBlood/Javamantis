class Prioridad:
	def __init__(self,numero,archivos,nombre):
		self.numero=numero
		self.archivos=archivos
		self.nombre=nombre

	def setArchivos(self,archivos):
		self.archivos=archivos

	def getArchivos(self):
		return self.archivos

	def setNumero(self,numero):
		self.numero=numero

	def setNombre(self,nombre):
		self.nombre=nombre

	def getNombre(self):
		return self.nombre
		
	def getNumero(self):
		return self.numero

	def setArchivosDic(self,archivosDic):
		self.archivosDic=archivosDic

	def getArchivosDic(self):
		return self.archivosDic

	def toArchivosDic(self):
		self.archivosDic=[]
		for l in self.archivos:
			self.archivosDic.append(l.asADict())

	def toDict(self):
		self.toArchivosDic()
		return {"Nombre":self.getNombre(),"Numero":self.getNumero(),"Archivos":self.getArchivosDic()}