from Json import Json
from Aplicaciones import Aplicaciones
from ArchivosValidos import ArchivosValidos
from CadenasBusqueda import CadenasBusqueda
from Prioridades import Prioridades
from Entornos import Entornos

class Configuracion(Json):

	def __init__(self,jsonRuta,jsonMongo=None):
		self.jsonR=jsonRuta
		self.json=Json(self.jsonR)
		self.openJson()
		if jsonMongo:
			json2=Json(jsonMongo).leer()
			self.clasificar(json2)
		else:
			self.clasificar(None)

	def openJson(self):
		self.jsonText=self.json.leer()

	def clasificar(self,mongo):
		self.clasificarApps()
		self.clasificarValidos()
		self.clasificarCadBusqueda(mongo)
		self.clasificarPrioridades()
		self.clasificarEntornos()
	
	def clasificarPrioridades(self):
		aux=[]
		for f in self.jsonText["prioridades"]:
			prior=Prioridades(f["numero"],f["expresion"],f["nombre"])
			aux.append(prior)
		self.setPrioridades(aux)

	def clasificarCadBusqueda(self,mongo):
		aux=[]
		for f in self.jsonText["cadenasBusqueda"]:
			cad=CadenasBusqueda(f["nombre"],f["cadena"],f["expresion"],f["extracciones"][0])
			aux.append(cad)
		if mongo:
			for f in mongo:
				aux.append(CadenasBusqueda("JNDI","DS",[f["Nombre"]],{}))
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

	def clasificarEntornos(self):
		aux=[]
		for f in self.jsonText["entornos"]:
			entorno=Entornos(f["nombre"],f["carpeta"])
			aux.append(entorno)
		self.setEntornos(aux)

	def setEntornos(self,entornos):
		self.entornos=entornos

	def setAplicaciones(self,aplicaciones):
		self.aplicaciones=aplicaciones

	def setArchivosValidos(self,archivos):
		self.archivosValidos=archivos

	def setCadenasBusqueda(self,cadenasBusqueda):
		self.cadenasBusqueda=cadenasBusqueda
		
	def setPrioridades(self,prioridades):
		self.prioridades=prioridades

	def getEntornos(self):
		return self.entornos

	def getAplicaciones(self):
		return self.aplicaciones

	def getArchivosValidos(self):
		return self.archivosValidos

	def getCadenasBusqueda(self):
		return self.cadenasBusqueda

	def getPrioridades(self):
		return self.prioridades