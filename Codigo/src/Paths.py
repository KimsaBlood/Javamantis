import os
from ArchivoOut import ArchivoOut
from Entornos import Entornos

class Paths:
	def __init__(self,carpetas,path,archivosValidos,entornos):
		self.path=path
		self.archivosValidos=archivosValidos
		self.carpetas=carpetas
		self.entornos=entornos
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
						entorno="ninguno"
						if os.path.isfile(os.path.join(r, file)):
							
							for l in self.archivosValidos:
								if l.getExtension() in file:
									for f in self.entornos:
										if f.getCarpeta() in os.path.join(r, file):
											entorno=f.getNombre()
									arch=ArchivoOut(os.path.join(r, file),l.getExtension(),l.getHardCode(),None,None,None,None,entorno)
									arch.leer()
									files.append(arch)
									i+=1
		else:
			for r, d, f in os.walk(self.path):
					for file in f:
						if os.path.isfile(os.path.join(r, file)):
							entorno="ninguno"
							for l in self.archivosValidos:
								if l.getExtension() in file:
									for f in self.entornos:
										if f.getCarpeta() in os.path.join(r, file):
											entorno=f.getNombre()
									print(entorno)
									arch=ArchivoOut(os.path.join(r, file),l.getExtension(),l.getHardCode(),None,None,None,None,entorno)
									arch.leer()
									files.append(arch)
									i+=1
		self.archivos=files

	def getArchivos(self):
		return self.archivos

	def setArchivos(self):
		return self.archivos