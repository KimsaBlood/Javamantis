class LineasOut:
	def __init__(self,numeroLinea,texto,extraccion=None,nomExtraccion=None):
		self.numeroLinea=numeroLinea
		self.texto=texto
		self.extraccion=extraccion
		self.nombreEx=nomExtraccion

	def setNomExtraccion(self,nomExtraccion):
		self.nombreEx=nomExtraccion

	def setNumeroLinea(self,numeroLinea):
		self.numeroLinea=numeroLinea

	def setTexto(self,texto):
		self.texto=texto

	def setExtraccion(self,url):
		self.extraccion=extraccion

	def getNomExtraccion(self):
		return self.nombreEx

	def getNumeroLinea(self):
		return self.numeroLinea

	def getTexto(self):
		return self.texto

	def getExtraccion(self):
		return self.extraccion

	def toDict(self):
		if self.getNomExtraccion():
			return {"Linea":self.getNumeroLinea(),"Texto":self.getTexto(),self.getNomExtraccion():self.getExtraccion()}
		else:
			return {"Linea":self.getNumeroLinea(),"Texto":self.getTexto()}
