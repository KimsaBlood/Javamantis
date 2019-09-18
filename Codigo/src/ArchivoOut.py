import codecs
import re
from LineasOut import LineasOut
from Extracciones import Extracciones
"""Clase que define la salida de los archivos con su informacion en el json"""
class ArchivoOut:

	def __init__(self,archivo=None,extension=None,hardcode=None,cadena=None,lineas=None,repeticiones=None,nombre=None,entorno=None):
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
		self.entorno=entorno

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

	def setEntorno(self,entorno):
		self.entorno=entorno

	def getLineasDict(self):
		return self.lineasDict

	def getEntorno(self):
		return self.entorno

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
			for l in cadena.getExpresion():
				if re.match( r''+l+'', f):
					line=LineasOut(j,f)
					for x in cadena.getExtracciones():
						for y in x.getExpresiones():
							patron = re.compile(y)
							#Buscamos la cadena en la linea del contenido
							matcher=patron.search(f)
							#si el objeto no esta vacio creamos un objeto del tipo LineasOut y le pasamos el numero de linea, el texto y la url
							if matcher:
								line=LineasOut(j,f,matcher.group(0),x.getNombre())
								break
					lineas.append(line)
					i+=1	

			
		#Si i es diferente a 0 setteamos los valores obtenidos
		if i!=0:	
			self.setNombre(cadena.getNombre())
			self.setRepeticiones(i)
			self.setCadena(cadena.getExpresion())
			self.setLineas(lineas)
		#Si es igual cero regresamos a vacia la lista de lineas
		else:
			self.setLineas([])
		
				#print(self.entorno)

	def leer(self):
		"""Lee todas las lineas contenidas en el archivo"""
		lines2=[]
		days_file = codecs.open(self.archivo,'r',encoding = "ISO-8859-1")
		lines=days_file.readlines()
		self.contenido=lines

	def asADict(self):
		"""Regresa en forma de diccionario el archivo con sus atributos"""
		self.AsLineasDict()
		return {"Archivo":self.getArchivo(),"Extension":self.getExtension(),"NombreCad":self.getNombre(),"Cadena":self.getCadena(),"Repeticiones":self.getRepeticiones(),"Hardcode":self.getHardCode(),"Lineas":self.getLineasDict(),"Entorno":self.getEntorno()}