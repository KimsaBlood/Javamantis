class ConfiguracionWAS():
	def __init__(self,celula,cluster,nodo,servidor):
		self.celula=celula
		self.cluster=cluster
		self.nodo=nodo
		self.servidor=servidor

	def setCelula(self,celula):
		self.celula=celula

	def setCluster(self,cluster):
		self.cluster=cluster

	def setNodo(self,nodo):
		self.nodo=nodo

	def setServidor(self,servidor):
		self.servidor=servidor

	def getCelula(self):
		return self.celula

	def getCluster(self):
		return self.cluster

	def getNodo(self):
		return self.nodo

	def getServidor(self):
		return self.servidor