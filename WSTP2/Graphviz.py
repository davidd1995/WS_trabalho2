# -*- coding: utf-8 -*-
from django.http import HttpResponse
from graphviz import Source
from app.staticvars.staticpaths import pathtocsv
import re

relations = []
triples = []
pathtocsv= pathtocsv
class Graphviz():
    def triples2dot(triples):
        dot = \
            """ 
            graph "grafo" { 
            overlap = "scale"; 
            """
        for s, p, o in triples:
            print(s+ " "+ p+" "+ o)
            dot = dot + ('%s -- %s [label=%s]\n' % (
                re.sub('[^A-Za-z0-9]+', '', s), re.sub('[^A-Za-z0-9]+', '', o), re.sub('[^A-Za-z0-9]+', '', p)))
        dot = dot + "}"
        return dot

    def tracegraph(dot):
        g = Source(dot, "relations.gv", "dotout", "pdf", "neato")

        g.render(view=True)
        with open('dotout/relations.gv.pdf', 'rb') as pdf:
            response = HttpResponse(pdf.read())
            response['content_type'] = 'application/pdf'
            response['Content-Disposition'] = 'attachment;filename=grafo.pdf'
            return response
