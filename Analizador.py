from Configuracion import Configuracion
from Paths import Paths
from AplicacionOut import AplicacionOut
import threading
import json
class Analizador:
	def __init__(self):
		pass

	def AnalizarThread(self,config,paths,l):
		"""Genera una aplicacion de salida"""
		self.appOut=AplicacionOut(paths,config,l.getNombre())
		self.appOut.generar()
			
	def Analizar(self):
		"""Crea objeto de configuracion y crea un thread por cada aplicaion de entrada"""
		config=Configuracion("config.json")
		for l in config.getAplicaciones():
			t=threading.Thread(target=self.AnalizarThread,args=(config,Paths(l.getRuta(),config.getArchivosValidos(),config.getCadenasBusqueda()),l))
			t.start()
class Main:
	def main():
		an=Analizador().Analizar()
	main()