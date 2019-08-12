class LineasOut:
	def __init__(self,numeroLinea,texto,url=None):
		self.numeroLinea=numeroLinea
		self.texto=texto
		self.url=url

	def setNumeroLinea(self,numeroLinea):
		self.numeroLinea=numeroLinea

	def setTexto(self,texto):
		self.texto=texto

	def setUrl(self,url):
		self.url=url

	def getNumeroLinea(self):
		return self.numeroLinea

	def getTexto(self):
		return self.texto

	def getUrl(self):
		return self.url

	def toDict(self):
		return {"Linea":self.getNumeroLinea(),"Texto":self.getTexto(),"Url":self.getUrl()}