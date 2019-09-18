import os
import re

class Binarios(object):

	#Inicializa la ruta con "."
	def __init__(self):
		self.ruta = "."
		self.incidencias = {}
	
	#Agrega la ruta de busqueda 
	def __init__(self, ruta):
		self.ruta = ruta
		self.incidencias = {}
	
	#Agrega la ruta de busqueda 
	def setRuta(self, ruta):
		self.ruta = ruta
		self.incidencias = {}
	
	#Analiza en caso de que el nomnre del binario no se encuentre 
	#en el build y este en un properties externo 
	def __fileExtra(self, var, fileName):
		archivo = fileName.replace("build.xml","build.properties")
		f = open (archivo,"r")
		lineas = f.readlines()
		for l in lineas:
			if var in l : 
				return l[l.find("=")+1:].strip()
		return "null"
		
	#Extrae el nombre de la propiedad en la que se encuentra el archivo
	#producido 
	def __extraeProp(self, prop, archivo, fileName):
		for l in archivo:
			match = re.search(r'name=.('+prop+').', l)
			if match :
				#print (l)
				coincide = l[l.find("value=")+7:]
				if (coincide.find("'")>= 0):
					return coincide[:coincide.find("'")]
				if (coincide.find('"')>= 0):
					return coincide[:coincide.find('"')]
		
		return self.__fileExtra(prop, fileName)
		
	#Extrae las propedades donde se configuea el nombre de los binario 
	#producidos por el build 
	def __extraeName(self, linea, extension, archivo, fileName):
		pf = linea.find (extension)
		if pf >= 0 :
			alto = 0
			pi = pf
			while (not alto) :
				if pi <= 0:
					return 'null'
				elif linea[pi] == '{' :
					variable = linea[pi+1:] 
					pr = pi + variable.find("}")+2 
					resto = ""
					if pr < pf :
						resto    = variable[pr:pf]
					variable = variable[:variable.find("}")]
					nombre   = self.__extraeProp(variable, archivo, fileName )
					return nombre + resto + extension
				elif linea[pi] == '"' :
					return linea[pi+1:pf]+extension
				elif linea[pi] == '/' :
					return linea[pi+1:pf]+extension
				pi -= 1
		else:
			return "null"

	#Busca los binario que se configuraron en el build y en el pom 
	def buscabinarios(self):
		path = self.ruta
		filesBuild = []
		filesPom   = []
		listaWars  = {}
		for root, directories, files in os.walk(path):
			for f in files:
				if 'build.xml' in f :
					filesBuild.append(os.path.join(root, f))
				if 'pom.xml'   in f :
					filesPom.append(os.path.join(root, f))
		
		for f in filesPom:
			#print (f)
			arch = open(f, "r")
			lineas = arch.readlines()
			for linea in lineas:
				if linea.find("<finalName>") >= 0 :
					value = linea[linea.find("<finalName>"):linea.find("</finalName>")].replace("<finalName>","").strip()
					if not "artifactId" in value: 
						value += ".war"	
						if (f in listaWars) :
							if not value in listaWars[f]:
								listaWars[f].append(value)
						else:
							listaWars[f] = []
							listaWars[f].append(value) 
			
		for f in filesBuild:
			arch = open(f, "r")
			lineas = arch.readlines()
			for linea in lineas:
				value = ""
				if linea.find ("<ear") >= 0:
					value = self.__extraeName(linea,".ear",lineas, f)
				elif linea.find("<war") >= 0:
					value = self.__extraeName(linea,".war",lineas, f)
				elif linea.find ("<jar") >=0 :
					value = self.__extraeName(linea,".war",lineas, f)
					value = self.__extraeName(linea,".ear",lineas, f)
				if value != "" and value != "null":
					#print (listaWars[f])
					if (f in listaWars) :
						if not value in listaWars[f]:
							listaWars[f].append(value)
					else:
						listaWars[f] = []
						listaWars[f].append(value)
		self.incidencias = listaWars
		listW=[]
		for l in listaWars.values():
			for m in l:
				if m not in listW:
					listW.append(m)
		return listW