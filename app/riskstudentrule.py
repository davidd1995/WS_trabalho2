# -*- coding: utf-8 -*-
from app.inferencerule import inferencerule

class riskstudent(inferencerule):
    def getqueries(self):
        risk = [('?p','age','?a'),
                ('?p','famsup','no')]
        return [risk]
    def maketriples(self,p,a):
        if (int(a)<18):
            return [(p,'risk','yes')]
        else:
            return []
