# -*- coding: utf-8 -*-

import csv

class Grafo:

    def __init__(self):
        self._spo = []

    def add(self, sub, pred, obj):
        if (sub,pred,obj) not in self._spo:
            self._spo.append((sub, pred, obj))

    def remove(self,sub, pred, obj):

        triples = self.triples(sub, pred, obj)
        for (s,p,o) in list(triples):
            self._spo.remove(tuple([s,p,o]))

    def triples(self, sub, pred, obj):
        try:
            if sub != None:
                if pred != None:
                    if obj != None:
                        for i in self._spo:
                            if i[0]==sub and i[1]==pred and i[2]==obj:
                                yield i
                    else:
                        for retObj in self._spo:
                            if retObj[0]==sub and retObj[1]==pred:
                                yield retObj
                else:
                    if obj != None:
                        for retPred in self._spo:
                            if retPred[0]==sub and retPred[2]==obj:
                                yield retPred
                    else:
                        for obj in self._spo:
                            if obj[0]== sub:
                                yield obj

            else:
                if pred != None:
                    if obj != None:
                        for retSub in self._spo:
                            if retSub[1]==pred and retSub[2]==obj:
                                yield retSub
                    else:
                        for retSub in self._spo:
                            if retSub[1]==pred:
                                yield retSub
                else:
                    if obj != None:
                        for retSub in self._spo:
                            if retSub[2]==obj:
                                yield retSub
                    else:
                        for retSub in self._spo:
                            yield retSub

        except KeyError:
            pass


    def load(self, filename):
        f = open(filename, 'r', encoding='utf-8')
        reader = csv.reader(f)
        for sub, pred, obj in reader:
            self.add(sub, pred, obj)
        f.close()

    def save(self, filename):
        f = open(filename, "w", encoding='utf-8')
        writer = csv.writer(f)
        for sub, pred, obj in self.triples(None, None, None):
            writer.writerow([sub, pred, obj])
        f.close()

    def query(self, clauses):
        bindings = None
        for clause in clauses:
            bpos = {}
            qc = []
            for pos, x in enumerate(clause):
                if x.startswith('?'):
                    qc.append(None)

                    bpos[x[1:]]=pos
                else:
                    qc.append(x)

            rows = list(self.triples(qc[0], qc[1], qc[2]))

            if bindings == None:
                bindings = []
                for row in rows:
                    binding = {}
                    for var, pos in bpos.items():
                        binding[var] = row[pos]
                    bindings.append(binding)
            else:
                newb = []
                for binding in bindings:
                    for row in rows:
                        validmatch = True
                        tempbinding = binding.copy()
                        for var, pos in bpos.items():
                            if var in tempbinding:
                                if tempbinding[var] != row[pos]:
                                    validmatch = False
                            else:
                                tempbinding[var] = row[pos]
                        if validmatch:
                            newb.append(tempbinding)
                bindings = newb
        return bindings


    def applyinference(self, rule):
        queries = rule.getqueries()
        bindings=[]
        for query in queries:
            bindings += self.query(query)
        for b in bindings:

            new_triples = rule.maketriples(str(b['p']),str(b['a']))
            for s,p,o in new_triples:
                self.add(s,p,o)

    def applyinferencehappy(self, rule):
        queries = rule.getqueries()
        bindings=[]
        for query in queries:
            bindings += self.query(query)
        for b in bindings:

            new_triples = rule.maketriples(str(b['p']),str(b['go']),str(b['alc']))
            for s,p,o in new_triples:
                self.add(s,p,o)

    def applyinferenceavailable(self, rule):
        queries = rule.getqueries()
        bindings=[]
        for query in queries:
            bindings += self.query(query)
        for b in bindings:

            new_triples = rule.maketriples(str(b['p']),str(b['p2']))
            for s,p,o in new_triples:
                self.add(s,p,o)


    def printAllTriples(self):
        t = self.triples(None, None, None)
        Grafo.printTriples(t)


    @staticmethod
    def printTriples(t):
        for el in t:
            print(("%15s --> %15s --> %15s" % el).encode())

    def printList(self, t):
        for dicionario in t:
            print(dicionario)