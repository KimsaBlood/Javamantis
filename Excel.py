from PrioridadesOut import PrioridadesOut
import xlsxwriter
class Excel():
	def __init__(self):
		self.workbook = xlsxwriter.Workbook('hello26.xlsx')

	def escribir(self):
		pass

	def leer(self):
		pass

	def setNombre(self):
		pass

	def getNombre(self):
		pass

	def getData(self):
		pass

	def setData(self):
		pass

	def setFormato(self):
		pass

	def cerrar(self):
		self.workbook.close()

	def addWorksheet(self,prioridades,name):
		count=1
		worksheet = self.workbook.add_worksheet(name[0:31])
		worksheet.write(0,0, "ARCHIVO")
		worksheet.write(0,1,"CADENA")
		worksheet.write(0,2,"LINEA")
		worksheet.write(0,3,"PRIORIDAD")
		print(name)
		for f in prioridades.getPriorList():
			for l in f.getArchivos():
				for x in l.getLineas():
					print(l.getArchivo())
					print(x.getTexto())
					worksheet.write(count,0, l.getArchivo())
					worksheet.write(count,1,x.getTexto())
					worksheet.write(count,2,x.getNumeroLinea())
					worksheet.write(count,3,f.getNumero())
					count+=1
		"""for f in range(1,len(prioridades)+3):
				for l in prioridades.getPriorList():
					for x in l.getArchivos():
						worksheet.write(count,0, l["archivo"])
						worksheet.write(count,1,x["texto"])
						worksheet.write(count,2,x["numeroLinea"])
						worksheet.write(count,3,str(f))
						count+=1"""