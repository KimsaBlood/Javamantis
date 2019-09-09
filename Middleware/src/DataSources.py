class DataSources():
	def __init__(self,nombre=None,ubicacion=None,id=None,propiedades=None):
		self.nombre=nombre
		self.ubicacion=ubicacion
		self.id=id
		self.propiedades=propiedades

	def setNombre(self,nombre):
		self.nombre=nombre

	def setUbicacion(self,ubicacion):
		self.ubicacion=ubicacion

	def setID(self,id):
		self.id=id

	def setPropiedades(self,propiedades):
		self.propiedades=propiedades

	def getNombre(self):
		return self.nombre

	def getUbicacion(self):
		return self.ubicacion

	def getID(self):
		return self.id

	def getPropiedades(self):
		return self.propiedades

	def getToJson(self):
		return {"Nombre":self.getNombre(),"Ubicacion":self.getUbicacion(),"ID":self.getID(),"Propiedades":self.getPropiedades()}