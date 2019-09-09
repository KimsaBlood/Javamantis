class Pila:
	def __init__(self):
		self.items = []
	
	def esVacia(self):
		return self.items == []
	
	def push(self, item):
		self.items.insert(0,item)

	def pop(self):
		if not self.esVacia():
			return self.items.pop(0)
	
	def top(self):
		return self.items[0]
	
	def tamano(self):
		return len(self.items)

	def printPila(self):
		for l in self.items:
			print(l)

	def vaciar(self):
		self.items=[]