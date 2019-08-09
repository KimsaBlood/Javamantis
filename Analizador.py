from Configuracion import Configuracion
from Paths import Paths
from AplicacionOut import AplicacionOut
import threading
from Excel import Excel
import json
class Analizador:
	def __init__(self):
		pass

	def AnalizarThread(self,config,paths,l,ex):
		"""Genera una aplicacion de salida"""
		self.appOut=AplicacionOut(paths,config,l.getNombre(),ex)
		self.appOut.generar()
			
	def Analizar(self):
		"""Crea objeto de configuracion y crea un thread por cada aplicaion de entrada"""
		ex=Excel()
		threads = list()
		count=1
		config=Configuracion("config.json")
		for l in config.getAplicaciones():
			t=threading.Thread(target=self.AnalizarThread,args=(config,Paths(l.getRuta(),config.getArchivosValidos(),config.getCadenasBusqueda()),l,ex,))
			threads.append(t)
			t.start()
			count+=1
		for count, thread in enumerate(threads):
			thread.join()
		ex.cerrar()
class Main:
	def main():
		an=Analizador().Analizar()
	main()