from Configuracion import Configuracion
from Paths import Paths
from PrioridadesOut import PrioridadesOut
from ArchivoOut import ArchivoOut
from Json import Json
from Excel import Excel

class AplicacionOut:
	
	def __init__(self,paths,config,nombre,excel):
		#tipo Path
		self.paths=paths
		#tipo Configuracion
		self.config=config
		#tipo string
		self.nombre=nombre
		#tipo list
		self.archivosAux=None
		self.excel=excel

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
		self.archivosAux=[]
		for l in self.paths.getArchivos():
			self.buscarPorArchivo(l,self.config.getCadenasBusqueda())
		self.prior=PrioridadesOut(self.getArchivosAux(),self.config.getPrioridades())
		self.prior.ordenar()
		Json.contenido(self.getNombre()+".json",self.toDict()).convertirAJson()
		self.excel.addWorksheet(self.prior,self.nombre)

	def buscarPorArchivo(self,archivo,cadenas):
		for l in cadenas:
			archivo.buscar(archivo.getContenido(),l)
			if archivo.getLineas():
				self.archivosAux.append(ArchivoOut(archivo.getArchivo(),archivo.getExtension(),archivo.getHardCode(),archivo.getCadena(),archivo.getLineas(),archivo.getRepeticiones(),archivo.getNombre()))
	
	def toDict(self):
		return {"Aplicacion":self.getNombre(),"Prioridades":self.prior.toDict()}