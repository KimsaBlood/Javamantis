from QueryMongoDB import QueryMongoDB

a = QueryMongoDB()

for aux in a.getURLS("Norkom"):
	print(aux)
