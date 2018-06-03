# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from app.grafo import Grafo #Triplestore
from app.staticvars.staticpaths import pathtocsv #String path to CSV file
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient

endpoint = "http://localhost:7200"
repo_name = "trabalho2"
client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)



query ="""
PREFIX baseProperty: <http://www.student-mat.com/pred/>
SELECT *
WHERE{
?s?p?o
Filter(isLiteral(?o))

}
"""
payload_query = {"query": query}
res = accessor.sparql_select(body=payload_query,
                             repo_name=repo_name)

res = json.loads(res)
