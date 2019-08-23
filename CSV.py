import codecs
from AplicacionesCSV import AplicacionesCSV
from opcionesCSV import opcionesCSV
from Json import Json
class CSV:
	def __init__(self,nombre):
		self.nombre=nombre

	def setNombre(self,nombre):
		self.nombre=nombre
	
	def getNombre(self):
		return self.nombre

	def leer(self):
		lines2=[]
		days_file = codecs.open(self.nombre,'r',encoding = "ISO-8859-1")
		lines=days_file.read().splitlines()
		self.contenido=lines

	def primerFiltro(self):
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
					app=AplicacionesCSV(l[:-2],opcs2)
					cad="true"
			else:
				if ":" in l and "&&" in l:
					if info:
						opcs2.append(opcionesCSV(info,opcs))
					info=[]
					ini=l.index("&&")
					fin=l.index(":")
					opcs=l[ini+2:fin]
					info.append(l[fin+1:])
				elif "&&" in l:
					ini=l.index("&&")
					info.append(l[ini+2:])
		
	def getOpcToJson(self,opciones):
		opcs=[]
		for l in opciones:
			#print(l.toDict())
			opcs.append(l.toDict())
		return opcs

	def getAppToJson(self):
		app=[]
		for l in self.apps2:
			app.append({"Nombre":l.getNombre(),"Opciones":self.getOpcToJson(l.getOpciones())})
		return app

	def getToJson(self):
		return {"Aplicaciones":self.getAppToJson()}

csv=CSV("DatosAplicacionesDeQA.txt")
csv.leer()
csv.primerFiltro()
js=Json("data.json",csv.getToJson())
js.convertirAJson()