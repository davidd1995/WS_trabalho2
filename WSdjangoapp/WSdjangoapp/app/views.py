# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
#from app.models import graph
from app.riskstudentrule import riskstudent
from app.unhappyrule import Unhappyrule
from app.relationavailablerule import relationavailable
import app.Graphviz
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
endpoint = "http://localhost:7200"
repo_name = "trabalho2"
client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)
bindings = []

def __init__(self):
    self._spo = []


def indexpage(request):

    query = """
    PREFIX baseProperty: <http://www.student-mat.com/pred/>
    PREFIX mov:<http://movies.org/pred/>
    PREFIX move: <http://movies.org/>
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

    for e in res['results']['bindings']:
        bindings.append((e['s']['value'],e['p']['value'],e['o']['value']))
    return render(request, 'index.html', {'tuples':bindings})


def sendinfo(request):
    provisoria=[]
    error = False
    c1 = request.POST['c1']

    if len(c1)==0:
        error = True
        return render(request,'index.html',{'errorsend':error})

    x = str(c1).split(" ")
    query1 = []

    for s in x:
        clauses=s[1:len(s)-1].split(",")
        query1.append((clauses[0],clauses[1],clauses[2]))
    print(clauses[0], clauses[1], clauses[2])
    if(clauses[0]=='?s' and clauses[2]=='?o'):
        query = """
            PREFIX baseProperty: <http://www.student-mat.com/pred/>
            PREFIX mov:<http://movies.org/pred/>
            PREFIX move: <http://movies.org/>
            SELECT *
            WHERE{
            """+clauses[0]+""" """+clauses[1]+""" """+clauses[2]+""".
            }
            """
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query,
                                     repo_name=repo_name)
        res = json.loads(res)

        print(res)
        for e in res['results']['bindings']:
            provisoria.append((e['s']['value'],clauses[1], e['o']['value']))
        print(provisoria)
        return render(request, 'index.html', {'tuples': provisoria})
    return 0# render(request, 'index.html', {'tuples': provisoria})

    #results = graph.query(query)
    #return render(request,'index.html',{'tuples':results})

def addtriple(request):
    error = False
    sub = request.POST['sub']
    pred = request.POST['pred']
    obj = request.POST['obj']

    if len(sub)==0 or len(pred)==0 or len(obj)==0 :
        error = True
        return render(request,'index.html',{'erroradd':error})

    update = """
    PREFIX mov:<http://movies.org/pred/>
    PREFIX move: <http://movies.org/>
    INSERT DATA
    {
     """+sub+""" """+pred+""" """+obj+""".
    }
    """
    payload_query = {"update": update}
    res = accessor.sparql_update(body=payload_query,
                                 repo_name=repo_name)
    bindings.append((sub,pred,obj))
    return render(request,'index.html',{'tuples':bindings,'erroradd':error})

def rmtriple(request):
    error = False
    sub = request.POST['sub']
    pred = request.POST['pred']
    obj = request.POST['obj']

    if len(sub)==0 or len(pred)==0 or len(obj)==0 :
        error = True
        return render(request,'index.html',{'errorrm':error})

    if (str(sub) == 'None' and str(pred) == 'None'):

        update = """
        PREFIX mov:<http://movies.org/pred/>
        PREFIX move: <http://movies.org/>
        DELETE DATA
        {
            ?s?p"""+obj+""". 
        }
        """
        payload_query = {"update": update}
        res = accessor.sparql_update(body=payload_query,
                                     repo_name=repo_name)
    elif (str(obj) == 'None' and str(pred) == 'None'):
        update = """
        PREFIX mov:<http://movies.org/pred/>
        PREFIX move: <http://movies.org/>
        DELETE DATA
        {
        """+sub+""""?p?o.
        }
        """
        payload_query = {"update": update}
        res = accessor.sparql_update(body=payload_query,
                                     repo_name=repo_name)


    elif (sub == 'None' and obj == 'None'):
        update = """
                PREFIX mov:<http://movies.org/pred/>
                PREFIX move: <http://movies.org/>
                DELETE DATA
                {
                """ + sub + """"?p?o.
                }
                """
        payload_query = {"update": update}
        res = accessor.sparql_update(body=payload_query,
                                     repo_name=repo_name)
    elif(str(sub)=='None'):
        update = """
                PREFIX mov:<http://movies.org/pred/>
                PREFIX move: <http://movies.org/>
                DELETE DATA
                {
                 ?s"""+pred+""" """+obj+""".
                }
                """
        payload_query = {"update": update}
        res = accessor.sparql_update(body=payload_query,
                                     repo_name=repo_name)
    elif (str(pred)=='None'):
        update = """
                PREFIX mov:<http://movies.org/pred/>
                PREFIX move: <http://movies.org/>
                DELETE DATA
                {
                """+sub+"""?p"""+obj+""".
                }
                """
        payload_query = {"update": update}
        res = accessor.sparql_update(body=payload_query,
                                     repo_name=repo_name)
    elif (str(obj)=='None'):
        update = """
                PREFIX mov:<http://movies.org/pred/>
                PREFIX move: <http://movies.org/>
                DELETE DATA
                {
                """+sub+""" """+pred+""""?p.
                }
                """
        payload_query = {"update": update}
        res = accessor.sparql_update(body=payload_query,
                                     repo_name=repo_name)

    else:
        update = """
                PREFIX mov:<http://movies.org/pred/>
                PREFIX move: <http://movies.org/>
                DELETE DATA
                {
                """+sub+""" """+pred+""" """+obj+""".
                }
                """
        payload_query = {"update": update}
        res = accessor.sparql_update(body=payload_query,
                                     repo_name=repo_name)

    bindings.clear()
    query = """
       PREFIX baseProperty: <http://www.student-mat.com/pred/>
       PREFIX mov:<http://movies.org/pred/>
       PREFIX move: <http://movies.org/>
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

    for e in res['results']['bindings']:
        bindings.append((e['s']['value'], e['p']['value'], e['o']['value']))
    return render(request, 'index.html', {'tuples': bindings})

    return render(request,'index.html',{'tuples':bindings,'errorrm':error})

def downloadgraphvis(request):
   # Graphviz.tracegraph()
    with open('app/dotout/relations.gv.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read())
        response['content_type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment;filename=grafo.pdf'
        return response

def inferenciarisco(request):
    risk = riskstudent()
    #graph.applyinference(risk)
    return 0 #render(request,'index.html',{'tuples':graph.query([('?a1','?b2','?c3')])})

def inferenciainfeliz(request):
    un = Unhappyrule()
    #graph.applyinferencehappy(un)
    return 0#render(request,'index.html',{'tuples':graph.query([('?a1','?b2','?c3')])})

def inferenciarelacao(request):
    av = relationavailable()
    #graph.applyinferenceavailable(av)
    return 0 #render(request,'index.html',{'tuples':graph.query([('?a1','?b2','?c3')])})