class LineasOut:
	def __init__(self,numeroLinea,texto):
		self.numeroLinea=numeroLinea
		self.texto=texto

	def setNumeroLinea(self,numeroLinea):
		self.numeroLinea=numeroLinea

	def setTexto(self,texto):
		self.texto=texto

	def getNumeroLinea(self):
		return self.numeroLinea

	def getTexto(self):
		return self.texto

	def toDict(self):
		return {"Linea":self.getNumeroLinea(),"Texto":self.getTexto()}