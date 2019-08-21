from Json import Json
from Aplicaciones import Aplicaciones
from ArchivosValidos import ArchivosValidos
from CadenasBusqueda import CadenasBusqueda
from Prioridades import Prioridades

class Configuracion(Json):

	def __init__(self,jsonRuta,jsonMongo):
		self.jsonR=jsonRuta
		self.json=Json(self.jsonR)
		self.openJson()
		json2=Json(jsonMongo).leer()
		self.clasificar(json2)

	def openJson(self):
		self.jsonText=self.json.leer()

	def clasificar(self,mongo):
		self.clasificarApps()
		self.clasificarValidos()
		self.clasificarCadBusqueda(mongo)
		self.clasificarPrioridades()
	
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
		for f in mongo["Aplicaciones"][0]["JNDI"]:
			if f["Tipo"] in "DataSources":
				aux.append(CadenasBusqueda("JNDI",f["Tipo"],[f["Name"]],{}))
		self.setCadenasBusqueda(aux)
		for x in aux:
			for l in x.getExpresion():
				print(l)

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