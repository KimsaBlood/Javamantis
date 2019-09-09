from opcionesWAS import opcionesWAS
class AplicacionesWAS:
	def __init__(self,nombre=None,opcs=None,info=None):
		self.nombre=nombre
		self.opciones=opcs

	def setNombre(self,nombre):
		self.nombre=nombre

	def getNombre(self):
		return self.nombre

	def setOpciones(self,opciones):
		self.opciones=opciones

	def getOpciones(self):
		return self.opciones

	def filtrarAplicaciones(self):
		cad="false"
		count=0
		apps=[]
		self.apps2=[]
		opcs=""
		opcs2=[]
		info=[]
		app=None
		for l in self.contenido:
			if l.endswith("&&"):
				if l[:-2] not in apps:
					apps.append(l[:-2])
					if app:
						self.apps2.append(app)
						opcs2=[]
					app=AplicacionesWAS(l[:-2].replace(" ","_"),opcs2)
					cad="true"
			else:
				if ":" in l and "&&" in l:
					if info:
						opcs2.append(opcionesWAS(info,opcs.replace(" ","_")))
					info=[]
					ini=l.index("&&")
					fin=l.index(":")
					opcs=l[ini+2:fin]
					info.append(l[fin+1:])
				elif "&&" in l:
					ini=l.index("&&")
					info.append(l[ini+2:])

	def configurarAplicaciones(self,celula,cluster,nodo,servidor):
		info=self.getInfoFromDB()
		conf=ConfiguracionWAS(celula,cluster,nodo,servidor)
		for l in info:
			apps=[]
			for x in l["Aplicaciones"]:
				opcs=[]
				for y in x["Opciones"]:
					opcs.append(opcionesWAS(y.values()[0],y.keys()[0]))
				apps.append(AplicacionesWAS(x["Nombre"],opcs))
				self.sustituir(AplicacionesWAS(x["Nombre"],opcs))
		print(len(apps))
	
	def sustituirAplicaciones(self,apps):#opcion server
		for l in apps.getOpciones():
			if "Server" in l.getNombre():
				for x in l.getInfo():
					print(x)

	def getOpcToJson(self,opciones):
		opcs=[]
		for l in opciones:
			opcs.append({l.getNombre():l.getInfo()})
		return opcs

	def getAppToJson(self):
		app=[]
		for l in self.apps2:
			app.append({"Nombre":l.getNombre(),"Opciones":self.getOpcToJson(l.getOpciones())})
		return app

	def getToJsonApps(self):
		return {"Aplicaciones":self.getAppToJson()}