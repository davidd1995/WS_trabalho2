# -*- coding: utf-8 -*-
from app.inferencerule import inferencerule
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json


class riskstudent(inferencerule):
    def __init__(self):
        self.baseEntity = "http://www.student-mat.com/entity/"
        self.baseProperty = "http://www.student-mat.com/pred/"
        self.endpoint = "http://localhost:7200"
        self.repo_name = "trabalho2"
        self.client = ApiClient(endpoint=self.endpoint)
        self.accessor = GraphDBApi(self.client)

    def get_triples(self):
        query = """
           PREFIX baseProperty: <http://www.student-mat.com/pred/>
           PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
           PREFIX baseStudent: <http://www.student-mat.com/class/>
           PREFIX baseEntity: <http://www.student-mat.com/entity/>
           PREFIX fb: <http://rdf.freebase.com/ns/>
           SELECT *
           WHERE {
               ?s baseProperty:age ?o .
               ?s baseProperty:famsup 'no' .
           }
              """
        payload_query = {"query": query}
        res = self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)
        res = json.loads(res)
        results = ""
        for result in res['results']['bindings']:
            sub = result['s']['value'].replace(self.baseEntity, '')
            age = float(result['o']['value'])
            if(int(age) <18):
                results += sub + ' risk ' + 'yes'+' .\n'
        return results