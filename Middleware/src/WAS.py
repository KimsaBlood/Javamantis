import codecs
from opcionesWAS import opcionesWAS
import sys
sys.path.insert(0, '../../Generales/src/')
from MongoDB import MongoDB
from Archivo import Archivo
from Pila import Pila
from Json import Json
from ConfiguracionWAS import ConfiguracionWAS
from pprint import pprint
from DataSources import DataSources
import re
class WAS:
	def __init__(self,nombreApps=None,nombreDS=None,nombreRes=None,nombreDeploys=None):
		self.nombreApps=nombreApps
		self.nombreDS=nombreDS
		self.nombreRes=nombreRes
		self.nombreDeploys=nombreDeploys
		self.mdb=MongoDB("Kimsa","localhost","27017")

	def setNombre(self,nombre):
		self.nombre=nombre
	
	def getNombre(self):
		return self.nombre

	def AnalizarAplicaciones(self):
		self.leer()
		self.filtrar()
		jsonWAS=self.getToJson()
		js=Json("data.json",jsonWAS)
		js.convertirAJson()
		#self.setInfoIntoDB(jsonWAS)

	def setInfoIntoDB(self,jsonWAS,colleccion):
		self.mdb.insertar(jsonWAS,colleccion)

	def getInfoFromDB(self):
		return self.mdb.consultar(collection)	

	def AnalizarDS(self):
		arch=Archivo(self.nombreDS)
		result=[]
		self.aux=1
		self.result2=[]
		self.pila=Pila()
		self.ramas=[]
		res=[]
		r=[]
		res2=[]
		res3=[]
		nombre=""
		for l in arch.leer():
			match = re.search(r'^([^\[\]]*):[^\[\]]*$', l)
			if l.startswith("&&"):
				if r:
					res2.append({nombre:r})
					r=[]
				nombre=l.replace("&&","")
			elif l.startswith("[") or l.startswith("#->") or match:
				r.append(l)
			elif l and not l.startswith("---"):
				r.append(l)
		if r:
			res2.append({nombre:r})
		for x in res2:
			for l in x:
				res3=[]
				if "Aplicaciones" in l:
					for y in x[l]:
						print(y)
				else:
					for y in x[l]:
						if y.startswith("#->"):
							if result:
								res3.append(result)
								result=[]
							o=self.getCabecera(y.replace("#->","").replace(")",""))
							result.append(o)
						elif y.startswith("["):
							o=self.filtrado(y.replace("[]","null"),[])
							result.append(o)
					js=Json(l+".json",{l:res3})
					js.convertirAJson()
					res.append({l:res3})
	
	def getAnalizar(self,contenido):
		pass
		
	def getCabecera(self,contenido):
		result2={}
		x=re.split("[#|\()]",contenido)
		if len(x)==4:
			result2.update({"Nombre":x[0]})
			result2.update({"Binario":x[1]})
			result2.update({"Deployment":x[3]})
		elif len(x)==1:
			result2.update({"Nombre":x[0]})
		return result2

	def checarRepeticiones(self,diccionario,valor):
		for key in valor.keys():
			if key in diccionario.keys():
				pass
	def filtrado(self,contenido,result2):
		pila=Pila()
		pila.push("inicio")
		result={}
		result3=[]
		r=[]
		p=0
		if self.esRama2(contenido):
			p=self.getIndexRama(contenido)-1
		r=self.cut3(contenido[p:],pila,contenido[p:],[],0)
		if r:
			for l in r:
				if self.esRama2(l):
					a=self.filtrado(l,[])
					if l==r[-1]:
						result2.append(a)
					else:
						for y in a:
							if type(y)==dict:
								result.update(y)
							else:
								pass#result2.append(y)
				else:
					u=self.getValores2(l)
					if len(u)>1:
						for x in u:
							result3.append(self.getValores3(x))
					else:
						self.checarRepeticiones(result,self.getValores3(l))
						result.update(self.getValores3(l))
						result3.append(result)
						result={}
		else:
			u=self.getValores2(contenido[p:])
			if len(u)>1:
				for x in u:
					result3.append(self.getValores3(x))
				
			else:
				self.checarRepeticiones(result,self.getValores3(contenido[p:]))
				result.update(self.getValores3(contenido[p:]))	
				result3.append(result)
		if self.esRama2(contenido):
			result2.append({self.getNombreRama(contenido):result3})
		else:
			result2.append({"Propiedades":result3})
		return result2


	def cut2(self,contenido,pila,original,x):	
		if not pila.esVacia() and contenido:
			match = re.search(r'^\[((\w)+(\s))+\[', contenido)
			match2= re.search(r'^\[\[',contenido)
			match3=re.search(r'^\[[^\[\]]+\]',contenido)
			match4=re.search(r'^\]',contenido)
			if match:
				if "inicio" in pila.top():
					pila.pop()
				init=contenido.index(match.group(0))+len(match.group(0)[:-1])
				pila.push("[")
				x+=init
				x=self.cut2(contenido[init:].strip(),pila,original,x)
			elif match2:
				init=contenido.index(match2.group(0))+len(match2.group(0)[:-1])
				pila.push("[")
				x+=init
				x=self.cut2(contenido[init:].strip(),pila,original,x)
			elif match3:
				init=contenido.index(match3.group(0))+len(match3.group(0))
				x+=len(match3.group(0))
				x=self.cut2(contenido[init:].strip(),pila,original,x)
			elif match4:
				init=contenido.index(match4.group(0))+len(match4.group(0))		
				pila.pop()
				x+=len(match4.group(0))
				x=self.cut2(contenido[init:].strip(),pila,original,x)
		else:
			pass#print("carayy")
		return x

	def cut22(self,contenido,pila,original,result,x):	
		if not pila.esVacia() and contenido:
			match = re.search(r'^\[((\w)+(\s))+\[', contenido)
			match2= re.search(r'^\[\[',contenido)
			match3=re.search(r'^\[[^\[\]]+\]',contenido)
			match4=re.search(r'^\]',contenido)
			if match:
				if "inicio" in pila.top():
					pila.pop()
				init=contenido.index(match.group(0))+len(match.group(0)[:-1])
				pila.push("[")
				
				x+=init
				pila2=Pila()
				pila2.push("inicio")
				w=self.cut2(contenido[init:].strip(),pila2,original,0)
				
				u=contenido[:w+init].count("] [")
				result.append(contenido[:w+init+u].strip())
				pila2=Pila()
				pila2.push("inicio")
				self.cut22(contenido[w+init+u:].strip(),pila,contenido[w+init+u:].strip(),result,0)
				if contenido.endswith(contenido[w+init+u:].strip()) and contenido!=original:
					result.append(contenido[w+init+u:].strip())
			elif match2:
				init=contenido.index(match2.group(0))+len(match2.group(0)[:-1])
				pila.push("[")
				x+=init
				self.cut22(contenido[init:].strip(),pila,original,result,x)
			elif match3:
				init=contenido.index(match3.group(0))+len(match3.group(0))
				x+=len(match3.group(0))
				self.cut22(contenido[init:].strip(),pila,original,result,x)
			elif match4:
				init=contenido.index(match4.group(0))+len(match4.group(0))		
				pila.pop()
				x+=len(match4.group(0))
				self.cut22(contenido[init:].strip(),pila,original,result,x)
		elif pila.esVacia() and contenido:
			if contenido!=original:
				result.append(original[:x+original[:x].count("] [")+1].strip())
				pila.vaciar()
				pila.push("inicio")
				w=original[x+original[:x].count("] [")+1:].strip()
				self.cut22(w,pila,w,result,x)
		else:
			pass
		return result

	def cut3(self,contenido,pila,original,result,x):	
		match = re.search(r'^\[((\w)+(\s))+\[', contenido)
		match2= re.search(r'^\[\[',contenido)
		match3=re.search(r'^\[[^\[\]]+\]',contenido)
		match4=re.search(r'^\]',contenido)
		if not pila.esVacia() and contenido:	
			if match:
				pila.push("[")
				result.append(original[:x+original[:x].count("] [")].strip())
				pila2=Pila()
				pila2.push("inicio")
				m=original[x+original[:x].count("] ["):].strip()
				y=self.cut2(m,pila,m,0)	
				pila2=Pila()
				pila2.push("inicio")
				aux=original[:x+original[:x].count("] [")].strip()
				u=self.cut22(m[:y+m[:y].count("] [")+2].strip(),pila2,m[:y+m[:y].count("] [")+2].strip(),[],0)
				for h in u:
					contenido=contenido.replace(h,"",1)
				contenido=contenido.replace(m[y+m[:y].count("] [")+2:].strip(),"",1)
				result.append(contenido.strip())
				for h in u:
					if h not in result:
						result.append(h)
				if m[y+m[:y].count("] [")+2:].strip():
					result.append(m[y+m[:y].count("] [")+2:].strip())				
			elif match2:
				if "inicio" in pila.top():
					pila.pop()
				init=contenido.index(match2.group(0))+len(match2.group(0)[:-1])
				pila.push("[")
				x+=init
				self.cut3(contenido[init:].strip(),pila,original,result,x)
			elif match3:
				if "inicio" in pila.top():
					pila.pop()
				init=contenido.index(match3.group(0))+len(match3.group(0))
				x+=len(match3.group(0))
				self.cut3(contenido[init:].strip(),pila,original,result,x)
			elif match4:
				init=contenido.index(match4.group(0))+len(match4.group(0))		
				pila.pop()
				x+=len(match4.group(0))
				self.cut3(contenido[init:].strip(),pila,original,result,x)
		elif pila.esVacia():
			pass#print("esVacia")
		return result

	def DSToJson(self):
		dsJson=[]
		for l in self.ds:
			dsJson.append(l.getToJson())
		return dsJson

	def esRama2(self,contenido):
		match = re.search(r'^\[((\w)+(\s))+\[', contenido)
		return match

	def tieneRama(self,contenido):
		match = re.search(r'\[((\w)+(\s))+\[', contenido)
		return match

	def getIndexRama(self,contenido):
		match = re.search(r'^\[((\w)+(\s))+\[', contenido)
		return len(match.group(0))	

	def getNombreRama(self,contenido):
		match = re.search(r'^\[((\w)+(\s))+\[', contenido)
		return match.group(1)

	def getValores2(self,contenido):
		match=[]
		for m in re.finditer(r'((?!.(\[\w+\s)+))(\[*(\[[^\[\]]+\][ ]*)+\]*)',contenido):
			match.append(m.group())
		return match

	def getValores3(self,contenido):
		match={}
		for m in re.finditer(r'\[[^\[\]]+\]',contenido):
			val=m.group().strip().split(" ",1)
			if len(val)==2:
				match.update({val[0].replace("[","").replace("]",""):val[1].replace("[","").replace("]","")})
			else:
				match.update({"valorE":val[0].replace("[","").replace("]","")})
		return match

	def esValor(self,contenido):
		match=re.search(r'^\[[^\[\]]+\]',contenido)
		return match

WAS=WAS(None,"../archivos/WAS/DatosQACompletos.txt")
#WAS=WAS(None,"../archivos/WAS/DeploymentsQA2.txt")
WAS.AnalizarDS()
#WAS.configurarAplicaciones("nueva","nueva","ueva","nueva")

"""mdb=MongoDB("Kimsa","localhost","27017")
mdb.insertar(jsonWAS,"intento1")"""
"""DatosAplicacionesDeQA.txt"""