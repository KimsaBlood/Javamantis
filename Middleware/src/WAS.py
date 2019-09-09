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
		for l in arch.leer():
			if l.startswith("#"):
				pass
			elif l.startswith("["):
				self.filtrado(l.replace("[]","null"))
		
		js=Json("dataDS.json",result)
		js.convertirAJson()
	
	def filtrado(self,contenido):
		if self.esRama2(contenido):
			pila=Pila()
			pila.push("inicio")
			result=[]
			x=0
			r=self.cut3(contenido[self.getIndexRama(contenido)-1:],pila,contenido[self.getIndexRama(contenido)-1:],result,x)
			print(r)
			for l in r:
				if self.esRama2(l):
					pila.vaciar()
					pila.push("inicio")
					result=[]
					x=0
					print("cut3")
					w=self.cut3(l[self.getIndexRama(l)-1:],pila,l[self.getIndexRama(l)-1:],result,x)
					print(w)
				elif self.tieneRama(l):
					pila.vaciar()
					pila.push("inicio")
					result=[]
					x=0
					w=self.cut3(l,pila,l,result,x)
					print(w)
				else:
					print("valores")



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
			print("carayy")
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
				print(original[:init+w+1])
				print(original[init+w+1:].strip())
				self.cut22(contenido[init:].strip(),pila,original,result,x)
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
		elif pila.esVacia():
			if contenido!=original:
				result.append(original[:x+original[:x].count("] [")+1].strip())
				result.append(original[x+original[:x].count("] [")+1:].strip())
		return result
#si es rama mandar a cut3, si en cut3 encuentra inicio de rama mandar a cut2
#luego  hacer for con el resultado de cut2 en cut3 y agregar cada valor al resultado de cut2
#de ahi el resultado de cut3 hacer lo mismo con cada elemento, si no es rama, sacar valores
	def cut3(self,contenido,pila,original,result,x):	
		match = re.search(r'^\[((\w)+(\s))+\[', contenido)
		match2= re.search(r'^\[\[',contenido)
		match3=re.search(r'^\[[^\[\]]+\]',contenido)
		match4=re.search(r'^\]',contenido)
		if not pila.esVacia() and contenido:	
			if match:
				print(contenido)
				pila.push("[")
				result.append(original[:x+original[:x].count("] [")].strip())
				pila2=Pila()
				pila2.push("inicio")
				m=original[x+original[:x].count("] ["):].strip()
				y=self.cut2(m,pila,m,0)
				result.append(m[:y+m[:y].count("] [")+2].strip())
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
			print("esVacia")
		return result

	def DSToJson(self):
		dsJson=[]
		for l in self.ds:
			dsJson.append(l.getToJson())
		return dsJson

	def filtrarGeneral(self,contenido):
		x=self.getRamasR(contenido)
		result2={}
		if x:
			for l in x:
				result=[]
				if self.esRama2(l):
					result.append(self.filtrarGeneral(l[self.getIndexRama(l):-2]))
					r=self.getValores2(l[self.getIndexRama(l):-2])
				else:
					r=self.getValores2(l)
				for y in r:
					result.append(self.getValores3(y))
				print(l)
				if self.esRama2(l):
					result2.update({self.getNombreRama(l):result})
				else:
					result2.update({"x":result})
		return result2

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
			val=m.group().strip().split(" ")
			match.update({val[0]:val[1]})
		return match

	def esValor(self,contenido):
		match=re.search(r'^\[[^\[\]]+\]',contenido)
		return match

	def getRamasR(self,contenido):
		match=[]
		unidos=[]
		pila=Pila()
		for m in re.finditer('(\[\w+\s)+(\[+[^\[\]]+\]+[ ]*)+',contenido):
			pila.vaciar()
			pila.push("inicio")
			rama=self.esRama(m.group(),pila)
			if rama==1:
				match.append(m.group())
			elif rama==0:
				unidos.append(m.group())
			else:
				pila.vaciar()
				pila.push("inicio")
				self.val=[]
				self.x=0
				x=self.cut(rama,pila,rama)
				if len(x)>1:
					if x[0]:
						unidos.append(x[0])
					unidos.append(m.group()[:m.group().rfind(x[0])])
					if x[1]:
						unidos.append(x[1])
				else:
					unidos.append(m.group()[:m.group(0).rfind(x[0])])
					unidos.append(x[0])
		if unidos:
			r=self.unir(unidos)
			for l in r:
				match.append(l)
		return match

	

	def cut(self,contenido,pila,original):	
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
				self.x+=init
				self.cut(contenido[init:].strip(),pila,original)
			elif match2:
				if "inicio" in pila.top():
					pila.pop()
				init=contenido.index(match2.group(0))+len(match2.group(0)[:-1])
				pila.push("[")
				self.x+=init
				self.cut(contenido[init:].strip(),pila,original)
			elif match3:
				init=contenido.index(match3.group(0))+len(match3.group(0))
				self.x+=len(match3.group(0))
				self.cut(contenido[init:].strip(),pila,original)
			elif match4:
				if "inicio" in pila.top():
					pila.pop()
					self.val.append(original)
				else:
					init=contenido.index(match4.group(0))+len(match4.group(0))		
					pila.pop()
					self.x+=len(match4.group(0))
					self.cut(contenido[init:].strip(),pila,original)
		else:
			if contenido!=original:
				self.val.append(original[:self.x+original.count("] [")])
				self.val.append(original[self.x+original.count("] ["):])
		return self.val

	def unir(self,unidos):
		unido=[]
		r=[]
		a=iter(unidos)
		pila=Pila()
		for l in a:
			pila.vaciar()
			pila.push("inicio")
			try:
				nextA=next(a)
				x=self.esRama(l.strip()+nextA,pila)
				if x==1:
					r.append(l+nextA)
				else:
					unido.append(l+nextA)
			except StopIteration as e:
				unido.append(l)
				break
		if not r:
			r=self.unir(unido)
		return r

	def esRama(self,contenido,pila):
		val=0
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
				val=self.esRama(contenido[init:].strip(),pila)
			elif match2:
				init=contenido.index(match2.group(0))+len(match2.group(0)[:-1])
				pila.push("[")
				val=self.esRama(contenido[init:].strip(),pila)
			elif match3:
				init=contenido.index(match3.group(0))+len(match3.group(0))
				val=self.esRama(contenido[init:].strip(),pila)
			elif match4:
				init=contenido.index(match4.group(0))+len(match4.group(0))		
				pila.pop()
				val=self.esRama(contenido[init:].strip(),pila)
		elif pila.esVacia() and contenido:
			return contenido
		elif pila.esVacia():
			return 1
		else:
			return 0
		return val

WAS=WAS(None,"../archivos/WAS/DeploymentsQA2.txt")
WAS.AnalizarDS()
#WAS.configurarAplicaciones("nueva","nueva","ueva","nueva")

"""mdb=MongoDB("Kimsa","localhost","27017")
mdb.insertar(jsonWAS,"intento1")"""
"""DatosAplicacionesDeQA.txt"""