class MongoDB:
	def _init_(self,bd,host,port):
		self.bd=bd
		self.host=host
		self.port=port

	def insertar(insertar):
		return posts.insert_one(insertar)

	def conectar():
		myclient = pymongo.MongoClient("mongodb://"+self.port+":"+self.port+"/")
		db = myclient[self.bd]