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
				self.filtrado(l.replace("[]","null"),result)
		
		js=Json("dataDS.json",result)
		js.convertirAJson()
	
	def filtrado(self,contenido,result2):
		pila=Pila()
		pila.push("inicio")
		result={}
		r=self.cut3(contenido[self.getIndexRama(contenido)-1:],pila,contenido[self.getIndexRama(contenido)-1:],[],0)
		print(r)
		if r:
			for l in r:
				print(l)
				if self.esRama2(l):
					pila.vaciar()
					pila.push("inicio")
					w=self.cut3(l[self.getIndexRama(l)-1:],pila,l[self.getIndexRama(l)-1:],[],0)
					print("vamos")
					a=self.filtrado(l,[])
					for y in a:
						result.update(y)
				elif self.tieneRama(l):
					pila.vaciar()
					pila.push("inicio")
					x=0
					w=self.cut3(l,pila,l,[],x)
				else:
					print(l)
					result.update(self.getValores3(l))
		else:
			result.update(self.getValores3(contenido[self.getIndexRama(contenido)-1:]))
		result2.append({self.getNombreRama(contenido):result})
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
			pass#result.append(original[x+original[:x].count("] [")+1:].strip())
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
				pila.push("[")
				result.append(original[:x+original[:x].count("] [")].strip())
				pila2=Pila()
				pila2.push("inicio")
				m=original[x+original[:x].count("] ["):].strip()
				y=self.cut2(m,pila,m,0)
					
				pila2=Pila()
				pila2.push("inicio")
				u=self.cut22(m[:y+m[:y].count("] [")+2].strip(),pila2,m[:y+m[:y].count("] [")+2].strip(),[],0)
				for h in u:
					result.append(h)
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
			val=m.group().strip().split(" ")
			match.update({val[0]:val[1]})
		return match

	def esValor(self,contenido):
		match=re.search(r'^\[[^\[\]]+\]',contenido)
		return match

WAS=WAS(None,"../archivos/WAS/DeploymentsQA2.txt")
WAS.AnalizarDS()
#WAS.configurarAplicaciones("nueva","nueva","ueva","nueva")

"""mdb=MongoDB("Kimsa","localhost","27017")
mdb.insertar(jsonWAS,"intento1")"""
"""DatosAplicacionesDeQA.txt"""