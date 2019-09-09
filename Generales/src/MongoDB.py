import pymongo
class MongoDB:
	def __init__(self,bd,host,port):
		self.bd=bd
		self.host=host
		self.port=port
		self.conectar()

	def insertar(self,insertar,collection):
		coll=self.db[collection]
		coll.insert(insertar,check_keys=False)
	
	def consultar(self,collection):
		return self.db[collection].find()

	def conectar(self):
		myclient = pymongo.MongoClient("mongodb://"+self.host+":"+self.port+"/")
		self.db = myclient[self.bd]