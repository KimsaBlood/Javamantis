#db.AplicacionesQA.find({"MapResRefToEJB.Resourcetype":"javax.sql.DataSource"},{"MapResRefToEJB.TargetResourceJNDIName":1}).pretty() #
#db.DataSourceQA.find({"Datos_Generales.Tipo":"DataSource"},{"Datos_Generales.Nombre":1, "Datos_Generales.Cluster":1}).pretty()
#db.DataSourceQA.find({"Datos_Generales.Tipo":"DataSource"},{"Descripcion.Propiedades.jndiName":1})

import sys
from pymongo import MongoClient
from bson import json_util

class QueryMongoDB:
    client = None
    db = None
    collection = None

    def __init__(self):
        #properties = Json("properties.json")
        #self.url = properties.obtenerJson()
        
        self.client = MongoClient('mongodb://192.168.15.137:27017')
        self.db = self.client['CoreIT']
        self.collection = self.db['DataSourceQA']


    def usarDB(self, baseDeDatos):
        self.db = self.client['CoreIT']
		
    def usarCollection(self, coleccion):
        self.collection = self.db[coleccion+"QA"]


    """
        Parametros de Entrada: 
            self (Objeto)       :  
            tipoRecurso (String | Default = javax.sql.DataSource)  : Nombre del tipo de recurso a obtener. Este nombre esta definido por wsadmin para WAS
        Parametros de Salida:
            recursos (List): Lista con los recursos 
        Funcionalidad:

        Excepciones lanzadas:
    """
    def obtenerRecursos(self, string_tipoRecurso):
        self.db = self.client['CoreIT']
        self.collection = self.db['AplicacionesQA']
        list_recursos = self.collection.find({"MapResRefToEJB.Resourcetype":string_tipoRecurso},{"MapResRefToEJB.TargetResourceJNDIName":1})

        self.client.close()
        return list_recursos

    """
        Parametros de Entrada: 
            self (Objeto)       :  
            tipoRecurso (String | Default = javax.sql.DataSource)  : Nombre del tipo de recurso a obtener. Este nombre esta definido por wsadmin para WAS
        Parametros de Salida:
            recursos (List): Lista con los recursos 
        Funcionalidad:

        Excepciones lanzadas:
    """
    def obtenerDatasourcePorAplicacion(self, str_Aplicacion):    
        json_Datasources = []
        list_cluster = self.obtenerClusterDeAplicacion(str_Aplicacion)

        self.collection = self.db['DataSourceQA']

        for cluster in list_cluster:
            #print(cluster)
            list_recursos = self.collection.find({"Datos_Generales.Tipo":"DataSource", "Datos_Generales.Cluster":{"$regex":cluster}},{"Descripcion.Propiedades.jndiName":1})
            for a in list_recursos:
                try:
                    #print("- 5: "+a['Descripcion']['Propiedades'][5]['jndiName'])
                    json_nombreDatasource = a['Descripcion']['Propiedades'][5]['jndiName']
                except:
                    #print("- 6: "+a['Descripcion']['Propiedades'][6]['jndiName'])
                    json_nombreDatasource = a['Descripcion']['Propiedades'][6]['jndiName']

                json_Datasources.append(json_nombreDatasource)
        self.client.close()
        
        return json_Datasources
    
    """
        Parametros de Entrada: 
            self (Objeto)       :  
            tipoRecurso (String | Default = javax.sql.DataSource)  : Nombre del tipo de recurso a obtener. Este nombre esta definido por wsadmin para WAS
        Parametros de Salida:
            recursos (List): Lista con los recursos 
        Funcionalidad:

        Excepciones lanzadas:
    """
    def obtenerTodosLosDatasource(self, string_nombreAplicacion):
        self.db = self.client['CoreIT']

        self.collection = self.db['DataSourceQA']
        list_recursos = self.collection.find({"Datos_Generales.Tipo":"DataSource"},{"Descripcion.Propiedades.jndiName":1})
        
        #for a in list_recursos:
        #    print(a)

        #self.collection = self.db['DataSourceQA']
        #list_recursos = self.collection.find({"Datos_Generales.Tipo":"DataSource"},{"Datos_Generales.Nombre":1, "Datos_Generales.Cluster":1})

        self.client.close()
        return list_recursos

    """
        Parametros de Entrada: 
            self (Objeto)       :  
            tipoRecurso (String | Default = javax.sql.DataSource)  : Nombre del tipo de recurso a obtener. Este nombre esta definido por wsadmin para WAS
        Parametros de Salida:
            recursos (List): Lista con los recursos 
        Funcionalidad:

        Excepciones lanzadas:
    """
    def obtenerClusterDeAplicacion(self, str_Aplicacion):
        list_cluster = []
        list_server = self.obtenerServersDeAplicacion(str_Aplicacion)

        for cluster in list_server:
            for aux in cluster['MapModulesToServers'] :
                list_cluster.append(self.separarClusterDeCadenaServer(aux['Server']))


        list_cluster = self.eliminarElementosDuplicados(list_cluster)

        return list_cluster
    """
        Parametros de Entrada: 
            self (Objeto)       :  
            tipoRecurso (String | Default = javax.sql.DataSource)  : Nombre del tipo de recurso a obtener. Este nombre esta definido por wsadmin para WAS
        Parametros de Salida:
            recursos (List): Lista con los recursos 
        Funcionalidad:

        Excepciones lanzadas:
    """
    def separarClusterDeCadenaServer(self, server):
        str_aux = server.split(",")
        str_aux1 = str_aux[1].split("+")
        str_aux2 = str_aux1[0].split("=")

        return str_aux2[1]
    
    """
        Parametros de Entrada: 
            self (Objeto)       :  
            tipoRecurso (String | Default = javax.sql.DataSource)  : Nombre del tipo de recurso a obtener. Este nombre esta definido por wsadmin para WAS
        Parametros de Salida:
            recursos (List): Lista con los recursos 
        Funcionalidad:

        Excepciones lanzadas:
    """
    def obtenerServersDeAplicacion(self, str_Aplicacion):
        uri = str_Aplicacion + ",WEB-INF/web.xml"
        self.db = self.client['CoreIT']
        self.collection = self.db['AplicacionesQA']
        list_server= self.collection.find({"MapModulesToServers.URI":uri},{"MapModulesToServers.Server":1})
        
        return list_server



    """
        Parametros de Entrada: 
            self (Objeto)       :  
            tipoRecurso (String | Default = javax.sql.DataSource)  : Nombre del tipo de recurso a obtener. Este nombre esta definido por wsadmin para WAS
        Parametros de Salida:
            recursos (List): Lista con los recursos 
        Funcionalidad:

        Excepciones lanzadas:
    """
    def eliminarElementosDuplicados(self, list_cluster):
        list_clusterNoDuplicados = list_cluster

        for i, cluster in enumerate(list_cluster):
            for j, clusterAux in enumerate(list_clusterNoDuplicados):
                if cluster == clusterAux and i != j:
                    del list_clusterNoDuplicados[j]
                    break
                      


        return list_clusterNoDuplicados


    """
        Parametros de Entrada: 
            self (Objeto)       :  
            tipoRecurso (String | Default = javax.sql.DataSource)  : Nombre del tipo de recurso a obtener. Este nombre esta definido por wsadmin para WAS
        Parametros de Salida:
            recursos (List): Lista con los recursos 
        Funcionalidad:

        Excepciones lanzadas:
    """
    def obtenerRoles(self):
        self.db = self.client['CoreIT']
        self.collection = self.db['DataSourceQA']
        list_recursos = self.collection.find({"Datos_Generales.Tipo":"DataSource"},{"Datos_Generales.Nombre":1})

        self.client.close()
        return list_recursos