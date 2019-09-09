from Prioridad import Prioridad
from ArchivoOut import ArchivoOut
import re
class PrioridadesOut:
	def __init__(self,archivos=None,prioridades=None):
		#tipo ArchivoOut
		self.archivos=archivos
		#tipo prioridad
		self.prioridades=prioridades
		self.priorList=None
		self.priorListDict=None
		self.archivos2=None

	def setArchivos(self,archivos):
		self.archivos=archivos

	def getArchivos(self):
		return self.archivos

	def getPriorList(self):
		return self.priorList

	def setPriorList(self,priorList):
		self.priorList=priorList

	def getPriorListDic(self):
		return self.priorListDict

	def setPriorListDic(self,priorListDic):
		self.priorListDict=priorListDict

	def ordenar(self):
		self.excluirPrioridades()
		self.hardCodePrior1()
		self.hardCodePrior2()

	def hardCodePrior1(self):
		archAux=[]
		for l in self.archivos2:
			if l.getHardCode() in "false":
				if l.getLineas():
					archAux.append(ArchivoOut(l.getArchivo(),l.getExtension(),l.getHardCode(),l.getCadena(),l.getLineas(),l.getRepeticiones(),l.getNombre()))
		self.priorList.append(Prioridad("1",archAux,"Sin hardcode"))

	def hardCodePrior2(self):
		archAux=[]
		for f in self.archivos2:
			if f.getHardCode() in "true":
				archAux.append(f)
		self.priorList.append(Prioridad("2",archAux,"HardCode"))

	def excluirPrioridades(self):	
		archPrior=[]
		self.archivos2=[]
		self.priorList=[]
		
		for f in self.prioridades:
			for l in self.archivos:
				count=0
				linePrior=[]
				linePrior2=[]
				for x in l.getLineas():
					if re.match( r''+f.getExpresion()+'', x.getTexto()):
						linePrior.append(x)
						count+=1
					else:
						linePrior2.append(x)
				if linePrior:
					archPrior.append(ArchivoOut(l.getArchivo(),l.getExtension(),l.getHardCode(),l.getCadena(),linePrior,count,l.getNombre()))
				if linePrior2:
					self.archivos2.append(ArchivoOut(l.getArchivo(),l.getExtension(),l.getHardCode(),l.getCadena(),linePrior2,l.getRepeticiones()-count,l.getNombre()))
			self.priorList.append(Prioridad(f.getNumero(),archPrior,f.getNombre()))

	def AsPriorDict(self):
		self.priorListDict=[]
		for l in self.priorList:
			self.priorListDict.append(l.toDict())

	def toDict(self):
		self.AsPriorDict()
		return self.getPriorListDic()