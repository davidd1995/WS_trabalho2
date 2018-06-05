# -*- coding: utf-8 -*-
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json


class Unhappyrule():
    def __init__(self):
        self.baseEntity = "http://www.student-mat.com/entity/"
        self.baseProperty = "http://www.student-mat.com/pred/"
        self.endpoint = "http://localhost:7200"
        self.repo_name = "trabalho2"
        self.client = ApiClient(endpoint=self.endpoint)
        self.accessor = GraphDBApi(self.client)

    def get_triples(self):
        print("unhappy")
        query = """
           PREFIX baseProperty: <http://www.student-mat.com/pred/>
           PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
           PREFIX baseStudent: <http://www.student-mat.com/class/>
           PREFIX baseEntity: <http://www.student-mat.com/entity/>
           PREFIX fb: <http://rdf.freebase.com/ns/>
           SELECT *
           WHERE {
               ?s baseProperty:romantic 'no' .
               ?s baseProperty:goout ?o .
               ?s baseProperty:walc ?al.
           }
              """
        payload_query = {"query": query}
        res = self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)
        res = json.loads(res)
        print(res)
        results = ""
        for result in res['results']['bindings']:
            sub = result['s']['value'].replace(self.baseEntity, '')
            goout = float(result['o']['value'])
            alc = float(result['al']['value'])
            if(int(goout) >2 and (int(alc)>1)):
                results += sub + ' state ' + 'unhappy;'
        return results

