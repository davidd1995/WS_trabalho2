# -*- coding: utf-8 -*-
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json

class orientation():
    def __init__(self):
        self.baseEntity = "http://www.student-mat.com/entity/"
        self.baseProperty = "http://www.student-mat.com/pred/"
        self.endpoint = "http://localhost:7200"
        self.repo_name = "trabalho2"
        self.client = ApiClient(endpoint=self.endpoint)
        self.accessor = GraphDBApi(self.client)

    def get_triples(self):
        query = """
                PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX foaf:<http://xmlns.com/foaf/0.1/>
                PREFIX pred:<http://www.student-mat.com/pred/>
                select ?s ?o where { 
                    ?s pred:available ?o .
                    ?s rdf:type foaf:Person .
                    ?o rdf:type foaf:Person .
                } 
                 """
        payload_query = {"query": query}
        res = self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)
        res = json.loads(res)
        results = ""
        for result in res['results']['bindings']:
            sub = result['s']['value'].replace(self.baseEntity, '')
            sub2 = result['o']['value'].replace(self.baseEntity, '')
            if(sub != sub2):
                results += sub + ' hetero ' + 'yes' + ';'+sub2 + ' hetero ' + 'yes' + ';'
        return results