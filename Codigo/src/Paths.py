import os
from ArchivoOut import ArchivoOut
class Paths:
	def __init__(self,carpetas,path,archivosValidos):
		self.path=path
		self.archivosValidos=archivosValidos
		self.carpetas=carpetas
		self.getTodosArchivos()

	def setPath(self,path):
		self.path=path

	def getPath(self):
		return self.path

	def getTodosArchivos(self):
		files=[]
		i=0
		if self.carpetas:
			for x in self.carpetas:
				pathAux=self.path+"/"+x
				for r, d, f in os.walk(pathAux):
					for file in f:
						if os.path.isfile(os.path.join(r, file)):
							for l in self.archivosValidos:
								if l.getExtension() in file:
									arch=ArchivoOut(os.path.join(r, file),l.getExtension(),l.getHardCode())
									arch.leer()
									files.append(arch)
									i+=1
		else:
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