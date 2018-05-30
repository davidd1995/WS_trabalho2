# -*- coding: utf-8 -*-
from app.inferencerule import inferencerule

class relationavailable(inferencerule):
    def getqueries(self):
        risk = [('?p','sex','M'),
                ('?p','romantic','no'),
                ('?p2','sex','F'),
                ('?p2','romantic','no')]
        return [risk]
    def maketriples(self,p,p2):
        return [(p,'available',p2)]
