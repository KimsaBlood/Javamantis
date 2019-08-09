import codecs
import re
from LineasOut import LineasOut
class ArchivoOut:
	def __init__(self,archivo=None,extension=None,hardcode=None,cadena=None,lineas=None,repeticiones=None,nombre=None):
		self.archivo=archivo
		self.extension=extension
		self.hardcode=hardcode
		self.lineas=lineas
		self.cadena=cadena
		self.repeticiones=repeticiones
		self.nombre=nombre

	def getArchivo(self):
		return self.archivo

	def getCadena(self):
		return self.cadena

	def getExtension(self):
		return self.extension

	def getLineas(self):
		return self.lineas

	def getNombre(self):
		return self.nombre

	def getRepeticiones(self):
		return self.repeticiones

	def getHardCode(self):
		return self.hardcode

	def getContenido(self):
		return self.contenido

	def setHardCode(self,hardcode):
		self.hardcode=hardcode

	def setArchivo(self,archivo):
		self.archivo=archivo

	def setCadena(self,cadena):
		self.cadena=cadena

	def setExtension(self,extension):
		self.extension=extension

	def setLineas(self,lineas):
		self.lineas=lineas

	def setNombre(self,nombre):
		self.nombre=nombre

	def setRepeticiones(self,repeticiones):
		self.repeticiones=repeticiones

	def setContenido(self,contenido):
		self.contenido=contenido

	def setLineasDict(self,lineasDict):
		self.lineasDict=lineasDict

	def getLineasDict(self):
		return self.lineasDict

	def AsLineasDict(self):
		self.lineasDict=[]
		for l in self.lineas:
			self.lineasDict.append(l.toDict())
	
	def buscar(self,contenido,cadena):
		j=i=0
		lineas=[]

		for f in contenido:

			j+=1
			if re.match( r''+cadena.getExpresion()+'', f):
				line=LineasOut(j,f)
				lineas.append(line)
				i+=1	
		if i!=0:	
			self.setNombre(cadena.getNombre())
			self.setRepeticiones(i)
			self.setCadena(cadena.getExpresion())
			self.setLineas(lineas)
		else:
			self.setLineas([])

	def leer(self):
		lines2=[]
		days_file = codecs.open(self.archivo,'r',encoding = "ISO-8859-1")
		lines=days_file.readlines()
		#print("Examinando archivo"+file)
		for f in lines:
			lines2.append(f.strip())
		self.contenido=lines2

	def asADict(self):
		self.AsLineasDict()
		return {"Archivo":self.getArchivo(),"Extension":self.getExtension(),"NombreCad":self.getNombre(),"Cadena":self.getCadena(),"Repeticiones":self.getRepeticiones(),"Hardcode":self.getHardCode(),"Lineas":self.getLineasDict()}