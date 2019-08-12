import codecs
import re
from LineasOut import LineasOut
"""Clase que define la salida de los archivos con su informacion en el json"""
class ArchivoOut:

	def __init__(self,archivo=None,extension=None,hardcode=None,cadena=None,lineas=None,repeticiones=None,nombre=None):
		"""Constructor"""
		#Tipo string
		self.archivo=archivo
		#Tipo string
		self.extension=extension
		#Tipo string
		self.hardcode=hardcode
		#Tipo lineas
		self.lineas=lineas
		#tipo string
		self.cadena=cadena
		#tipo int
		self.repeticiones=repeticiones
		#tipo string
		self.nombre=nombre

	#getters y setters
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
		"""Asigna en una lista todos los objetos linea de forma para que se genere un json valido"""
		self.lineasDict=[]
		for l in self.lineas:
			self.lineasDict.append(l.toDict())
	
	def buscar(self,cadena):
		j=i=0
		lineas=[]
		#Recorremos la lista con el contenido del archivo
		for f in self.contenido:
			j+=1
			#Checamos si coincide con la expresion regular
			if re.match( r''+cadena.getExpresion()+'', f):
				#creamos un objeto con una epresion regular para extraer las url
				patron = re.compile("([-|:|\\\\|\w]+:\/\/)(\w*[.|:|/|@|\-|,|=|?|\\\\]*\w*)*")
				#Buscamos la cadena en la linea del contenido
				matcher=patron.search(f)
				#si el objeto no esta vacio creamos un objeto del tipo LineasOut y le pasamos el numero de linea, el texto y la url
				if matcher:
					line=LineasOut(j,f,matcher.group(0))
				else:
					#si es vacio usamos el segundo filtro para url (url progress por ejemplo)
					patron = re.compile("(.*url.*=\/\/)(\w*[.|:|/|@|\-|,|=|?|\\\\]*\w*)*")
					matcher=patron.search(f)
					#Si no es vacio mandamos el valor de url
					if matcher:
						line=LineasOut(j,f,matcher.group(0))
					#Si es vacio solo pasamos el numero de linea y el contenido d la linea
					else:
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
		for f in lines:
			lines2.append(f.strip())
		self.contenido=lines2

	def asADict(self):
		self.AsLineasDict()
		return {"Archivo":self.getArchivo(),"Extension":self.getExtension(),"NombreCad":self.getNombre(),"Cadena":self.getCadena(),"Repeticiones":self.getRepeticiones(),"Hardcode":self.getHardCode(),"Lineas":self.getLineasDict()}