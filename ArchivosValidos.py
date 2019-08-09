class ArchivosValidos:
	def __init__(self,extension,hardCode):
		self.extension=extension
		self.hardCode=hardCode

	def setExtension(self,extension):
		self.extension=extension

	def setHardCode(self,hardcode):
		self.hardCode=hardcode

	def getExtension(self):
		return self.extension

	def getHardCode(self):
		return self.hardCode