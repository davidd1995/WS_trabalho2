# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from app.OrientationQuery import orientation
from app.Query_sparql import query_sparql
from app.UnhappyQuery import Unhappyrule
from app.TinderQuery import relationavailable
from app.RiskstudentQuery import riskstudent
from Graphviz import Graphviz
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient

endpoint = "http://localhost:7200"
repo_name = "trabalho2"
client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)
bindings = []


_sparql = query_sparql()

baseEntity = "http://www.student-mat.com/entity/"
baseProperty = "http://www.student-mat.com/pred/"

def __init__(self):
    self._spo = []


def indexpage(request):
    template = loader.get_template('index.html')
    tuples = _sparql.list_all_triples()
    tuples = get_type(tuples)
    tuples = get_triples(tuples)
    context = {'tuples': tuples}
    return HttpResponse(template.render(context, request))



def sendinfo(request):
    baseEntity = "http://www.student-mat.com/entity/"
    baseProperty = "http://www.student-mat.com/pred/"


    provisoria=[]
    error = False
    c1 = request.POST['c1']

    if len(c1)==0:
        error = True
        return render(request,'index.html',{'errorsend':error})

    x = str(c1).split(" ")
    query1 = []
    space = " "

    for s in x:
        clauses=s[1:len(s)-1].split(",")
        query1.append((clauses[0],clauses[1],clauses[2]))
    if (clauses[0]=='?s' and clauses[1]=='?p' and clauses[2]!='?o'):
        query = """
                    PREFIX pred: <http://www.student-mat.com/pred/>
                    PREFIX entity: <http://www.student-mat.com/entity/>
                    SELECT *
                    WHERE{
                        """ + clauses[0] + """ """ + clauses[1]+ space + """\""""+clauses[2]+ """\"""" + """ .
                    }
                    """
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query,
                                     repo_name=repo_name)
        res = json.loads(res)

        for e in res['results']['bindings']:
            sub = e['s']['value'].replace(baseEntity, '').title()
            pred = e['p']['value'].replace(baseProperty, '').title()
            provisoria.append((sub, pred, clauses[2]))

    elif (clauses[2]=='?o' and clauses[1]=='?p' and clauses[0]!='?s'):
        query = """
                    PREFIX pred: <http://www.student-mat.com/pred/>
                    PREFIX entity: <http://www.student-mat.com/entity/>
                    SELECT *
                    WHERE{
                        entity:""" + clauses[0] + """ """ + clauses[1] + space + """ """ + clauses[2] + """ .
                    }
                    """
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query,
                                     repo_name=repo_name)
        res = json.loads(res)

        triples = []
        for e in res['results']['bindings']:
            obj = e['o']['value'].replace(baseEntity, '').title()
            pred = e['p']['value'].replace(baseProperty, '').title()
            provisoria.append((clauses[0], pred, obj))

    elif (clauses[0]=='?s' and clauses[2]=='?o' and clauses[1]!='?p'):
        query = """
                    PREFIX pred: <http://www.student-mat.com/pred/>
                    PREFIX entity: <http://www.student-mat.com/entity/>
                    SELECT *
                    WHERE{
                        """ + clauses[0] + """ pred:""" + clauses[1] + space + """ """ + clauses[2] + """ .
                    }
                    """
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query,
                                     repo_name=repo_name)
        res = json.loads(res)

        triples = []
        for e in res['results']['bindings']:
            sub = e['s']['value'].replace(baseEntity, '').title()
            obj = e['o']['value'].replace(baseEntity, '').title()
            provisoria.append((sub, clauses[1], obj))
    elif (clauses[0]=='?s' and clauses[2]!='?o' and clauses[1]!='?p'):
        query = """
                   PREFIX pred: <http://www.student-mat.com/pred/>
                   PREFIX entity: <http://www.student-mat.com/entity/>
                   SELECT *
                   WHERE{
                       """ + clauses[0] + """ pred: """ + clauses[1] + space + """\"""" + clauses[2] + """\"""" + """ .
                   }
                   """
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query,
                                     repo_name=repo_name)
        res = json.loads(res)

        triples = []
        for e in res['results']['bindings']:
            sub = e['s']['value'].replace(baseEntity, '').title()
            provisoria.append((sub, clauses[1], clauses[2]))
    elif (clauses[1]=='?p' and clauses[2]!='?o' and clauses[0]!='?s'):
        query = """
                   PREFIX pred: <http://www.student-mat.com/pred/>
                   PREFIX entity: <http://www.student-mat.com/entity/>
                   SELECT *
                   WHERE{
                       entity:""" + clauses[0] + """ """ + clauses[1] + space + """\"""" + clauses[2] + """\"""" + """ .
                   }
                   """
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query,
                                     repo_name=repo_name)
        res = json.loads(res)

        triples = []
        for e in res['results']['bindings']:
            pred = e['p']['value'].replace(baseEntity, '').title()
            provisoria.append((clauses[0], pred, clauses[2]))
    elif (clauses[2]=='?o' and clauses[0]!='?s' and clauses[1]!='?p'):
        query = """
                PREFIX pred: <http://www.student-mat.com/pred/>
                PREFIX entity: <http://www.student-mat.com/entity/>
                SELECT *
                WHERE{
                    entity:""" + clauses[0] + """ pred:""" + clauses[1] + space + """ """ + clauses[2] + """ .
                }
                """
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query,
                                     repo_name=repo_name)
        res = json.loads(res)

        triples = []
        for e in res['results']['bindings']:
            obj = e['o']['value'].replace(baseEntity, '').title()
            provisoria.append((clauses[0], clauses[1], obj))
    else:
        query = """
            PREFIX pred: <http://www.student-mat.com/pred/>
            PREFIX entity: <http://www.student-mat.com/entity/>
            SELECT *
            WHERE{
                """ + clauses[0] + """ """ + clauses[1]+space+ """ """+clauses[2]+ """ .
            }
            """
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query,
                                     repo_name=repo_name)
        res = json.loads(res)


        for e in res['results']['bindings']:
            sub = e['s']['value'].replace(baseEntity, '').title()
            pred = e['p']['value'].replace(baseProperty, '').title()
            obj = e['o']['value'].replace(baseEntity, '').title()
            provisoria.append((sub, pred, obj))

    tuples = get_type(provisoria)
    tuples = get_triples(tuples)
    context = {'tuples': tuples}
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

def addtriple(request):

    context = {'predicates': _sparql.get_all_predicates()}
    template = loader.get_template('index.html')
    if ('sub' and 'pred' and 'obj') in request.POST:
        sub = request.POST['sub']
        pred = request.POST['pred']
        obj = request.POST['obj']
        if sub and pred and obj:
            if _sparql.triple_already_exists(sub, pred):
                context.update({'error': True, 'message': 'Triple already exists'})
            else:
                _sparql.add_sparql(sub, pred, obj)
                context.update({'error': False, 'message': 'Triple successfully added'})
        else:
            context.update({'error': True, 'message': 'Fill all the fields'})
    else:
        context.update({'error': False})
    template = loader.get_template('index.html')
    tuples = _sparql.list_all_triples()
    tuples = get_type(tuples)
    tuples = get_triples(tuples)
    context = {'tuples': tuples}
    return HttpResponse(template.render(context, request))

def rmtriple(request):
    template = loader.get_template('index.html')
    if ('sub' and 'pred' and 'obj') in request.POST:
        sub = request.POST['sub']
        pred = request.POST['pred']
        obj = request.POST['obj']
        if sub and pred and obj:
            _sparql.rm_sparql(sub, pred, obj)
    else:
        context = {'error': False}
    template = loader.get_template('index.html')
    tuples = _sparql.list_all_triples()
    tuples = get_type(tuples)
    tuples = get_triples(tuples)
    context = {'tuples': tuples}
    return HttpResponse(template.render(context, request))


def downloadgraphvis(request):
    template = loader.get_template('index.html')
    dot=Graphviz.triples2dot(_sparql.list_all_triples())
    Graphviz.tracegraph(dot)
    with open('dotout/relations.gv.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read())
        response['content_type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment;filename=grafo.pdf'
        return response


def inferenciarisco(request):

    template = loader.get_template('index.html')
    rType = riskstudent()
    triples = rType.get_triples()
    _sparql.add_inferences(triples)
    tuples = _sparql.list_all_triples()
    tuples = get_type(tuples)
    tuples = get_triples(tuples)
    context = {'tuples': tuples}
    return HttpResponse(template.render(context, request))

def inferenciainfeliz(request):
    template = loader.get_template('index.html')
    rType = Unhappyrule()
    triples = rType.get_triples()
    _sparql.add_inferences(triples)
    tuples = _sparql.list_all_triples()
    tuples = get_type(tuples)
    tuples = get_triples(tuples)
    context = {'tuples': tuples}
    return HttpResponse(template.render(context, request))

def inferenciarelacao(request):
    template = loader.get_template('index.html')
    rType = relationavailable()
    triples = rType.get_triples()
    _sparql.add_inferences(triples)
    tuples = _sparql.list_all_triples()
    tuples = get_type(tuples)
    tuples = get_triples(tuples)
    context = {'tuples': tuples}
    return HttpResponse(template.render(context, request))

def inferenciaorientação(request):
    template = loader.get_template('index.html')
    rType = orientation()
    triples = rType.get_triples()
    _sparql.add_inferences(triples)
    tuples = _sparql.list_all_triples()
    tuples = get_type(tuples)
    tuples = get_triples(tuples)
    context = {'tuples': tuples}
    return HttpResponse(template.render(context, request))

def get_type(triples):
    res = []
    for sub, pred, obj in triples:
        if baseEntity in obj:
            res.append((sub, pred, obj, 'entity'))
        else:
            res.append((sub, pred, obj, 'literal'))
    return res

def get_triples(tuples):
    res = []
    for sub, pred, obj, obj_type in tuples:
        sub_res = sub.replace(baseEntity, '').replace('_', ' ').title()
        pred_res = pred.replace(baseProperty, '').replace('_', ' ').title()
        if baseEntity in obj:
            obj_res = obj.replace(baseEntity, '').replace('_', ' ').title()
            res.append((sub_res, pred_res, obj_res, obj_type))
        else:
            res.append((sub_res, pred_res, obj, obj_type))
    return res