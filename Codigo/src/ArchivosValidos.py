class ArchivosValidos:
	"""Clase definida por los archivosValidos en el archivo de configuracion"""
	def __init__(self,extension,hardCode):
		"""Constructor, extension del tipo string, hardCode del tipo string"""
		self.extension=extension
		self.hardCode=hardCode

	#getters y setters
	def setExtension(self,extension):
		self.extension=extension

	def setHardCode(self,hardcode):
		self.hardCode=hardcode

	def getExtension(self):
		return self.extension

	def getHardCode(self):
		return self.hardCode