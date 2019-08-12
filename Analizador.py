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
		"""Crea objeto de configuracion y crea un thread por cada aplicacion de entrada"""
		#Creamos un objeto del tipo Excel donde se crea un nuevo archivo
		ex=Excel()
		threads = list()
		count=1
		config=Configuracion("config.json")
		#Recorremos la lista de objetos Aplicacion en config y creamos un hilo por cada objeto
		for l in config.getAplicaciones():
			#Creamos el hilo y un objeto como parametro del tipo paths 
			t=threading.Thread(target=self.AnalizarThread,args=(config,Paths(l.getCarpetas(),l.getRuta(),config.getArchivosValidos()),l,ex,))
			threads.append(t)
			t.start()
			count+=1
		#Esperamos a que terminen todos los hilos paa cerrar el archivo excel
		for count, thread in enumerate(threads):
			thread.join()
		#cerramos el excel 
		ex.cerrar()

class Main:
	def main():
		an=Analizador().Analizar()
	main()