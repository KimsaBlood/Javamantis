import os
from ArchivoOut import ArchivoOut
class Paths:
	def __init__(self,path,archivosValidos,cadenas):
		self.path=path
		self.archivosValidos=archivosValidos
		self.getTodosArchivos(cadenas)

	def setPath(self,path):
		self.path=path

	def getPath(self):
		return self.path

	def getTodosArchivos(self,cadenas):
		files=[]
		i=0
		for r, d, f in os.walk(self.path):
			for file in f:
				if os.path.isfile(os.path.join(r, file)):
					for l in self.archivosValidos:
						if l.getExtension() in file:
							arch=ArchivoOut(os.path.join(r, file),l.getExtension(),l.getHardCode())
							arch.leer()
							files.append(arch)
							i+=1
		self.archivos=files

	def getArchivos(self):
		return self.archivos

	def setArchivos(self):
		return self.archivos