#db.AplicacionesQA.find({"MapResRefToEJB.Resourcetype":"javax.sql.DataSource"},{"MapResRefToEJB.TargetResourceJNDIName":1}).pretty() 
#db.DataSourceQA.find({"Datos_Generales.Tipo":"DataSource"},{"Datos_Generales.Nombre":1, "Datos_Generales.Cluster":1}).pretty()
#db.DataSourceQA.find({"Datos_Generales.Tipo":"DataSource"},{"Descripcion.Propiedades.jndiName":1})
#db.DataSourceQA.find({"Descripcion.Propiedades.jndiName":{$regex:"Exp"}},{"Datos_Generales.Nombre":1} ).pretty()

#db.AplicacionesQA.find("MapResRefToEJB.TargetResourceJNDIName":"mds.war,WEB-INF/web.xml"}).pretty() 

import sys
import re
from pymongo import MongoClient
from bson import json_util
#from Json import Json 

class QueryMongoDB:
    client = None
    db = None
    collection = None

    def __init__(self):
        #properties = Json("properties.json")
        #self.url = properties.obtenerJson()
        
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['CoreIT']
        self.collection = self.db['Data SourceQA']

    def getURLS(self, str_applicationName):
        db = self.client['Pruebas']
        collection = db[str_applicationName]
        list_urls = collection.find({"$or":[{"Prioridades.Numero":1}, {"Prioridades.Numero":2}]},{"Prioridades.Archivos.Lineas.url":1})

        return list_urls



    """
        Parametros de Entrada: 
            self (Objeto)       :  
            tipoRecurso (String | Default = javax.sql.DataSource)  : Nombre del tipo de recurso a obtener. Este nombre esta definido por wsadmin para WAS
        Parametros de Salida:
            recursos (List): Lista con los recursos 
        Funcionalidad:

        Excepciones lanzadas:
    """
    def getApplicationDatasourcesJndis(self, str_application):    
        #print("App: " + str_application)
        json_Datasources = []
        list_cluster = self.getClustersNames(str_application)

        self.collection = self.db['DataSourceQA']
        
        for cluster in list_cluster:
            #print("-Cluster: " + cluster)
            list_recursos = self.collection.find({"Datos_Generales.Tipo":"DataSource", "Datos_Generales.Cluster":{"$regex":cluster}},{"Descripcion.Propiedades.jndiName":1})
            for a in list_recursos:
                try:
                    #print("-> 5: "+a['Descripcion']['Propiedades'][5]['jndiName'])
                    json_nombreDatasource = a['Descripcion']['Propiedades'][5]['jndiName']
                except:
                    #print("-> 6: "+a['Descripcion']['Propiedades'][6]['jndiName'])
                    json_nombreDatasource = a['Descripcion']['Propiedades'][6]['jndiName']

                json_Datasources.append(json_nombreDatasource)
        self.client.close()
        
        return json_Datasources


    def getApplicationDatasourcesNames(self, str_application):    
        #print("App: " + str_application)
        json_Datasources = []
        list_cluster = self.getClustersNames(str_application)

        self.collection = self.db['DataSourceQA']
        
        for cluster in list_cluster:
            #print("-Cluster: " + cluster)
            list_recursos = self.collection.find({"Datos_Generales.Tipo":"DataSource", "Datos_Generales.Cluster":{"$regex":cluster} },{"Datos_Generales.Nombre":1})
            for a in list_recursos:
                #print("-> ds: "+a['Datos_Generales']['Nombre'])
                json_nombreDatasource = a['Datos_Generales']['Nombre']
              

                json_Datasources.append(json_nombreDatasource)
        self.client.close()
        
        return json_Datasources
    def getApplicationResourceReference(self, str_application):
        self.collection = self.db['AplicacionesQA']
        json_mapResRefToEJB= self.collection.find({"MapResRefToEJB.URI":{"$regex":str_application}},{"MapResRefToEJB.ResourceReference":1})
        list_resourceReference = []

        for json_resourceReference in json_mapResRefToEJB:
            for aux in json_resourceReference["MapResRefToEJB"]:
                list_resourceReference.append(aux["ResourceReference"])

        return list_resourceReference

    """
        Parametros de Entrada: 
            tipoRecurso (String | Default = javax.sql.DataSource)  : Nombre del tipo de recurso a obtener. Este nombre esta definido por wsadmin para WAS
        Parametros de Salida:
            recursos (List): Lista con los recursos 
        Funcionalidad:

        Excepciones lanzadas:
    """
    def getClustersNames(self, str_application):
        list_clusters = []
        json_server = self.getServers(str_application)
        
        for json_mapModulesToServers in json_server:
            for server in json_mapModulesToServers['MapModulesToServers'] :
                str_serverName = server['Server']
                list_foundClusters = re.findall("cluster\w+", str_serverName)
                list_clusters.extend(list_foundClusters)

        list_clusters = self.deleteRepeated(list_clusters)

        return list_clusters

    """
        Parametros de Entrada: 
            tipoRecurso (String | Default = javax.sql.DataSource)  : Nombre del tipo de recurso a obtener. Este nombre esta definido por wsadmin para WAS
        Parametros de Salida:
            recursos (List): Lista con los recursos 
        Funcionalidad:

        Excepciones lanzadas:
    """
    def getServers(self, str_application):
        self.collection = self.db['AplicacionesQA']
        json_server= self.collection.find({"MapModulesToServers.URI":{"$regex":str_application}},{"MapModulesToServers.Server":1})
        
        return json_server



    """
        Parametros de Entrada: 
            list_repeated (Lista)  : Lista con elementos repetidos
        Parametros de Salida:
            list_noRepeated (List): Lista sin elementos repetidos
        Funcionalidad:

        Excepciones lanzadas:
    """
    def deleteRepeated(self, list_repeated):
        list_noRepeated = list_repeated

        for i, item_repeated in enumerate(list_repeated):
            for j, item_noRepeated in enumerate(list_noRepeated):
                if item_noRepeated == item_repeated and i != j:
                    del list_noRepeated[j]
                    break

        return list_noRepeated
