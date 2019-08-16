from Json import Json
from Aplicaciones import Aplicaciones
from ArchivosValidos import ArchivosValidos
from CadenasBusqueda import CadenasBusqueda
from Prioridades import Prioridades

class Configuracion(Json):

	def __init__(self,jsonRuta):
		self.jsonR=jsonRuta
		self.json=Json(self.jsonR)
		self.openJson()
		self.clasificar()

	def openJson(self):
		self.jsonText=self.json.leer()

	def clasificar(self):
		self.clasificarApps()
		self.clasificarValidos()
		self.clasificarCadBusqueda()
		self.clasificarPrioridades()
	
	def clasificarPrioridades(self):
		aux=[]
		for f in self.jsonText["prioridades"]:
			prior=Prioridades(f["numero"],f["expresion"],f["nombre"])
			aux.append(prior)
		self.setPrioridades(aux)

	def clasificarCadBusqueda(self):
		aux=[]
		for f in self.jsonText["cadenasBusqueda"]:
			cad=CadenasBusqueda(f["nombre"],f["cadena"],f["expresion"],f["extracciones"])
			aux.append(cad)
		self.setCadenasBusqueda(aux)

	def clasificarValidos(self):
		aux=[]
		for f in self.jsonText["archivosValidos"]:
			arch=ArchivosValidos(f["extension"],f["hardcode"])
			aux.append(arch)
		self.setArchivosValidos(aux)

	def clasificarApps(self):
		aux=[]
		for f in self.jsonText["aplicaciones"]:
			app=Aplicaciones(f["nombre"],f["ruta"],f["carpetas"])
			aux.append(app)
		self.setAplicaciones(aux)

	def setAplicaciones(self,aplicaciones):
		self.aplicaciones=aplicaciones

	def setArchivosValidos(self,archivos):
		self.archivosValidos=archivos

	def setCadenasBusqueda(self,cadenasBusqueda):
		self.cadenasBusqueda=cadenasBusqueda

	def setPrioridades(self,prioridades):
		self.prioridades=prioridades

	def getAplicaciones(self):
		return self.aplicaciones

	def getArchivosValidos(self):
		return self.archivosValidos

	def getCadenasBusqueda(self):
		return self.cadenasBusqueda

	def getPrioridades(self):
		return self.prioridades