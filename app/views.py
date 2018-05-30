# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from app.models import graph
from app.riskstudentrule import riskstudent
from app.unhappyrule import Unhappyrule
from app.relationavailablerule import relationavailable
import app.Graphviz



def indexpage(request):
    return render(request,'index.html',{'tuples':graph.query([('?a1','?b2','?c3')])})

def sendinfo(request):
    error = False
    c1 = request.POST['c1']

    if len(c1)==0:
        error = True
        return render(request,'index.html',{'errorsend':error})

    x = str(c1).split(" ")
    query = []
    for s in x:
        clauses=s[1:len(s)-1].split(",")
        query.append((clauses[0],clauses[1],clauses[2]))


    results = graph.query(query)
    return render(request,'index.html',{'tuples':results})

def addtriple(request):
    error = False
    sub = request.POST['sub']
    pred = request.POST['pred']
    obj = request.POST['obj']

    if len(sub)==0 or len(pred)==0 or len(obj)==0 :
        error = True
        return render(request,'index.html',{'erroradd':error})

    graph.add(str(sub),str(pred),str(obj))
    return render(request,'index.html',{'tuples':graph.query([('?a1','?b2','?c3')]),'erroradd':error})

def rmtriple(request):
    error = False
    sub = request.POST['sub']
    pred = request.POST['pred']
    obj = request.POST['obj']

    if len(sub)==0 or len(pred)==0 or len(obj)==0 :
        error = True
        return render(request,'index.html',{'errorrm':error})

    if (str(sub) == 'None' and str(pred) == 'None'):
        graph.remove(None, None, str(obj))
    elif (str(obj) == 'None' and str(pred) == 'None'):
        graph.remove(str(sub), None, None)
    elif (sub == 'None' and obj == 'None'):
        graph.remove(None, str(pred), None)
    elif(str(sub)=='None'):
        graph.remove(None,str(pred),str(obj))
    elif (str(pred)=='None'):
        graph.remove(str(sub), None, str(obj))
    elif (str(obj)=='None'):
        graph.remove(str(sub), str(pred), None)
    else:
        graph.remove(str(sub), str(pred), str(obj))

    return render(request,'index.html',{'tuples':graph.query([('?a1','?b2','?c3')]),'errorrm':error})

def downloadgraphvis(request):
    Graphviz.tracegraph()
    with open('app/dotout/relations.gv.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read())
        response['content_type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment;filename=grafo.pdf'
        return response

def inferenciarisco(request):
    risk = riskstudent()
    graph.applyinference(risk)
    return render(request,'index.html',{'tuples':graph.query([('?a1','?b2','?c3')])})

def inferenciainfeliz(request):
    un = Unhappyrule()
    graph.applyinferencehappy(un)
    return render(request,'index.html',{'tuples':graph.query([('?a1','?b2','?c3')])})

def inferenciarelacao(request):
    av = relationavailable()
    graph.applyinferenceavailable(av)
    return render(request,'index.html',{'tuples':graph.query([('?a1','?b2','?c3')])})