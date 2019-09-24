from JNDI import JNDI
from QueryMongoDB import QueryMongoDB
class JNDIS:
	def __init__(self):
		self.jndis=[]

	def getJNDIS(self):
		return self.jndis

	def setJNDIS(self,jndis):
		self.jndis=jndis

	def mongoJNDIS(self,lista,binario):
		names=[]
		if lista:
			for x in lista:
				if x not in names:
					names.append(x)
					self.jndis.append(JNDI(x,"(.*)"+x+"(.*)","JNDIS",binario))
	
	def mongoDSNames(self,lista,binario):
		names=[]
		if lista:
			for x in lista:
				if x not in names:
					names.append(x)
					self.jndis.append(JNDI(x,"(.*)"+x+"(.*)","DSNames",binario))

	def mongoRF(self,lista,binario):
		names=[]
		if lista:
			for x in lista:
				if x not in names:
					names.append(x)
					self.jndis.append(JNDI(x,"(.*)"+x+"(.*)","ResourceRef",binario))

	def getJNDIS(self,binariosList):
		querysMongo=QueryMongoDB()
		for x in binariosList:
			self.mongoJNDIS(querysMongo.getApplicationDatasourcesJndis(x),x)
			self.mongoDSNames(querysMongo.getApplicationDatasourcesNames(x),x)
			self.mongoRF(querysMongo.getApplicationResourceReference(x),x)
		print(self.jndis)
		return self.jndis

	def encontrados(self):
		encontrados=[]
		for l in self.jndis:
			if l.getEncontrado():
				if l not in encontrados:
					encontrados.append(l)
		return encontrados

	def encontradosToDict(self):
		encontrados=self.encontrados()
		json=[]
		for l in encontrados:
			json.append(l.toDict())
		return json