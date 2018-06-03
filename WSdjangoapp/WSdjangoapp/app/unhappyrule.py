# -*- coding: utf-8 -*-
from app.inferencerule import inferencerule

class Unhappyrule(inferencerule):
    def getqueries(self):
        risk = [('?p','romantic','no'),
                ('?p','goout','?go'),
                ('?p','Walc','?alc')]
        return [risk]
    def maketriples(self,p,go,alc):

        if (int(go)>2 and (int(alc)>1)):
            return [(p,'state','unhappy')]
        else:
            return []
