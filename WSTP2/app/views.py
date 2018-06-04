# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from app.Query_sparql import Query_sparl
from app.unhappyrule import Unhappyrule
from app.relationavailablerule import relationavailable
from app.riskstudentrule import riskstudent
import app.Graphviz
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
endpoint = "http://localhost:7200"
repo_name = "trabalho2"
client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)
bindings = []


_sparql = Query_sparl()
triples_platform = []


def __init__(self):
    self._spo = []


def indexpage(request):
    template = loader.get_template('index.html')
    context = {'triples': _sparql.list_all_triples()}
    return HttpResponse(template.render(context, request))



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
            PREFIX pred: <http://www.student-mat.com/pred/>
            PREFIX entity: <http://www.student-mat.com/entity/>
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

def addtriple(request):
    print("entra")
    context = {'predicates': _sparql.get_all_predicates()}
    template = loader.get_template('index.html')
    if ('sub' and 'pred' and 'obj') in request.POST:
        sub = request.POST['sub']
        pred = request.POST['pred']
        obj = request.POST['obj']
        print(sub+" "+ pred +" "+obj)
        if sub and pred and obj:
            if _sparql.triple_already_exists(sub, pred):
                context.update({'error': True, 'message': 'Triple already exists'})
            else:
                print("atualizou")
                _sparql.add_tosparl(sub, pred, obj)
                context.update({'error': False, 'message': 'Triple successfully added'})
        else:
            context.update({'error': True, 'message': 'Fill all the fields'})
    else:
        context.update({'error': False})
    template = loader.get_template('index.html')
    context = {'triples': _sparql.list_all_triples()}
    return HttpResponse(template.render(context, request))
    #return render(request,'index.html',{'tuples':bindings,'erroradd':error})

def rmtriple(request):
    print("entra")

    template = loader.get_template('index.html')
    if ('sub' and 'pred' and 'obj') in request.POST:
        sub = request.POST['sub']
        pred = request.POST['pred']
        obj = request.POST['obj']
        if sub and pred and obj:
            if sub.lower() == 'none':
                sub = None
            if pred.lower() == 'none':
                pred = None
            if obj.lower() == 'none':
                obj = None
            number = _sparql.rm_tosparl(sub, pred, obj)
            context = {'error': False, 'message': str(number) + ' triples were removed'}
        else:
            context = {'error': True, 'message': 'Fill all the fields'}
    else:
        context = {'error': False}
    template = loader.get_template('index.html')
    context = {'triples': _sparql.list_all_triples()}
    return HttpResponse(template.render(context, request))


def downloadgraphvis(request):
   # Graphviz.tracegraph()
    with open('app/dotout/relations.gv.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read())
        response['content_type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment;filename=grafo.pdf'
        return response

def inferenciarisco(request):

    template = loader.get_template('index.html')
    rType = riskstudent()
    triples = rType.get_triples()
    print(triples)
    _sparql.add_inferences(triples)
    for triple in triples.split('\n'):
        triple = triple.split(' ')
        if len(triple) >= 3:
            triples_platform.append((triple[0], triple[1], triple[2]))
    context = {'triples': _sparql.list_all_triples()}
    context.update({'triples': triples_platform})
    return HttpResponse(template.render(context, request))
    '''query = """
    PREFIX baseProperty: <http://www.student-mat.com/pred/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX baseStudent: <http://www.student-mat.com/class/>
    PREFIX baseEntity: <http://www.student-mat.com/entity/>
    PREFIX fb: <http://rdf.freebase.com/ns/>
    CONSTRUCT {
        ?s baseProperty:risk 'yes'.
    }
    WHERE {
        ?s baseProperty:age ?o .
        ?s baseProperty:famsup 'no' .
        FILTER (?o<'18')
    }
       """

    payload_query = {"query": query}

    res = accessor.sparql_select(body=payload_query,
                                 repo_name=repo_name)
    print(res)
    #res2 = json.loads(res)


   # for e in res2['results']['bindings']:
       # bindings.append((e['s']['value'], e['p']['value'], e['o']['value']))
    return 0 # render(request, 'index.html', {'tuples': bindings})
    #risk = riskstudent()
    #graph.applyinference(risk)
    #return render(request,'index.html',{'tuples':graph.query([('?a1','?b2','?c3')])})'''

def inferenciainfeliz(request):
    template = loader.get_template('index.html')
    rType = Unhappyrule()
    triples = rType.get_triples()
    print(triples)
    _sparql.add_inferences(triples)
    for triple in triples.split('\n'):
        triple = triple.split(' ')
        if len(triple) >= 3:
            triples_platform.append((triple[0], triple[1], triple[2]))
    context = {'triples': _sparql.list_all_triples()}
    context.update({'triples': triples_platform})
    return HttpResponse(template.render(context, request))

def inferenciarelacao(request):
    template = loader.get_template('index.html')
    rType = relationavailable()
    triples = rType.get_triples()
    _sparql.add_inferences(triples)
    for triple in triples.split('\n'):
        triple = triple.split(' ')
        if len(triple) >= 3:
            triples_platform.append((triple[0], triple[1], triple[2]))
    context = {'triples': _sparql.list_all_triples()}
    context.update({'triples': triples_platform})
    return HttpResponse(template.render(context, request))
