import sys
sys.path.insert(0, '../../Generales/src/')
from Configuracion import Configuracion
from Paths import Paths
from AplicacionOut import AplicacionOut
import threading
#from Excel import Excel
from Json import Json
from MongoDB import MongoDB
from pprint import pprint
from Prioridad import Prioridad
from PrioridadesOut import PrioridadesOut
from LineasOut import LineasOut
from ArchivoOut import ArchivoOut
from Binarios import Binarios
from CadenasBusqueda import CadenasBusqueda

from JNDIS import JNDIS
class Analizador:
	def __init__(self):
		pass

	def getBinarios(self,path):
		binario=Binarios(path)
		return binario.buscabinarios()
	
	def getURLSobrantes(self):
		pass

	def AnalizarThread(self,config,paths,l):
		"""Genera una aplicacion de salida"""
		mdb=MongoDB("Generales","localhost","27017")
		jndis=JNDIS()
		jndisLista=[]
		jndisLista=jndis.getJNDIS(self.getBinarios(paths.getPath()))
		self.appOut=AplicacionOut(paths,config,l.getNombre(),None,jndisLista)
		self.appOut.generar()
		x=jndis.encontradosToDict()
		y=[]
		y=objetoC.metodoCharly(x)
		for l in y:
			x.append(l)
		self.jsonJNDIS.append({"Aplicacion":l.getNombre(),"JNDIS":x})
			
	def Analizar(self):
		"""Crea objeto de configuracion y crea un thread por cada aplicacion de entrada"""
		#Creamos un objeto del tipo Excel donde se crea un nuevo archivo
		
		threads = list()
		config=Configuracion("../../Codigo/archivos/config.json")
		#Recorremos la lista de objetos Aplicacion en config y creamos un hilo por cada objeto
		for l in config.getAplicaciones():
			#Creamos el hilo y un objeto como parametro del tipo paths 
			t=threading.Thread(target=self.AnalizarThread,args=(config,Paths(l.getCarpetas(),l.getRuta(),config.getArchivosValidos(),config.getEntornos()),l,))
			threads.append(t)
			t.start()
			
	def Excel(self):
		ex=Excel()
		config=Configuracion("../../Codigo/archivos/config.json","../../Codigo/archivos/Datasources.json")
		mdb=MongoDB("Kimsa","localhost","27017")
		for l in config.getAplicaciones():
			for document in mdb.consultar(l.getNombre()): 
				priors=[]
				for f in document["Prioridades"]:
					archs=[]
					for x in f["Archivos"]:
						lineas=[]
						for y in x["Lineas"]:
							if len(y)==3:
								lineas.append(LineasOut(y["Linea"],y["Texto"],y.values()[0],y.keys()[0]))
							else:
								lineas.append(LineasOut(y["Linea"],y["Texto"]))
						archs.append(ArchivoOut(x["Archivo"],x["Extension"],x["Hardcode"],x["Cadena"],lineas,x["Repeticiones"],x["NombreCad"]))
					priors.append(Prioridad(f["Numero"],archs,f["Nombre"]))
				prior=PrioridadesOut()
				prior.setPriorList(priors)
				ex.addWorksheet(prior,l.getNombre())
		ex.cerrar()

class Main:
	def main():
		an=Analizador().Analizar()
		#Analizador().Excel()
	main()