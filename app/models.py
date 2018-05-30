# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from app.grafo import Grafo #Triplestore
from app.staticvars.staticpaths import pathtocsv #String path to CSV file
import pandas as pd

relations = []
triples = []
pathtocsv = pathtocsv

def maketriples(filepath):
    counter = 1
    csvfile = pd.read_csv(filepath)
    csvfile.drop_duplicates(inplace=True, keep='first')
    for row in csvfile:
        relations.append(row)

    for relation in relations:
        for value in csvfile[relation]:
            triples.append((str(counter), str(relation), str(value)))
            counter += 1
        counter = 1
    return triples

graph = Grafo()
triples=maketriples(pathtocsv)


for triple in triples:
    graph.add(str(triple[0]),str(triple[1]),str(triple[2]))
