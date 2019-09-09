from Configuracion import Configuracion
from Paths import Paths
from PrioridadesOut import PrioridadesOut
from ArchivoOut import ArchivoOut
from Json import Json
from Excel import Excel
from MongoDB import MongoDB

class AplicacionOut:
	
	def __init__(self,paths,config,nombre,excel=None):
		#tipo Path
		self.paths=paths
		#tipo Configuracion
		self.config=config
		#tipo string
		self.nombre=nombre
		#tipo list, se pone None en el constructor para evitar problemas con los apuntadores
		self.archivosAux=None
		#tipo excel
		self.excel=excel
		#tipo mongoDB
		self.mdb=MongoDB("Kimsa","localhost","27017")

	"""getters y setters"""
	def setPaths(self,paths):
		self.paths=paths

	def setNombre(self,nombre):
		self.nombre=nombre

	def setPrioridades(self,prioridades):
		self.prioridades=prioridades

	def setArchivosAux(self,archivosAux):
		self.archivosAux=archivosAux

	def getPaths(self):
		return self.paths

	def getNombre(self):
		return self.nombre

	def getPrioridades(self):
		return self.prioridades

	def getArchivosAux(self):
		return self.archivosAux

	def generar(self):
		"""Mandamos a llamar buscar por archivo y generamos las prioridades que tendra nuestra aplicacion de salida, se genera el json con ella"""
		#Inicializamos archivosAux en tipo lista vacia
		self.archivosAux=[]
		#recorremos la lista de archivos contenida en el objeto paths
		for l in self.paths.getArchivos():
			self.buscarPorArchivo(l,self.config.getCadenasBusqueda())
		#Generamos el contenido de las prioridades
		self.prior=PrioridadesOut(self.getArchivosAux(),self.config.getPrioridades())
		#Ordenamos el contenido en la prioridad correspondiente
		self.prior.ordenar()
		#Creamos un objeto json con el contenido y el nombre del archivo con su ruta y despues lo convertimos todo a un json
		Json.contenido("../../Codigo/Resultado/"+self.getNombre()+".json",self.toDict()).convertirAJson()
		#self.mdb.insertar(self.toDict(),self.nombre)

	def generarExcel():
		#Llamamos el metodo para abrir un libro en el excel abierto
		self.excel.addWorksheet(self.prior,self.nombre)

	def generarExcelMongo(self):
		pass

	def buscarPorArchivo(self,archivo,cadenas):
		"""Buscamos dentro del archivo todas las cadenas a buscar"""
		#recorremos la lista de cadenas
		for l in cadenas:
			#Mandamos llamar el metodo buscar
			archivo.buscar(l)
			#Si al momento de buscar encontro coincidencias el objeto lineas no estara vacio
			if archivo.getLineas():
				#Agregamos al atributos archivosAux del tipo lista de ArchivoOut un nuevo objeto del tipo para evitar problemas de apuntadores
				self.archivosAux.append(ArchivoOut(archivo.getArchivo(),archivo.getExtension(),archivo.getHardCode(),archivo.getCadena(),archivo.getLineas(),archivo.getRepeticiones(),archivo.getNombre()))
	
	def toDict(self):
		"""Convierte a tipo diccionario el objeto para mejorar su renderizacion a json"""
		return {"Aplicacion":self.getNombre(),"Prioridades":self.prior.toDict()}