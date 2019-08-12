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
		worksheet.write(0,4,"URL")
		for f in prioridades.getPriorList():
			for l in f.getArchivos():
				for x in l.getLineas():
					worksheet.write(count,0, l.getArchivo())
					worksheet.write(count,1,x.getTexto())
					worksheet.write(count,2,x.getNumeroLinea())
					worksheet.write(count,3,f.getNumero())
					worksheet.write(count,3,x.getUrl())
					count+=1