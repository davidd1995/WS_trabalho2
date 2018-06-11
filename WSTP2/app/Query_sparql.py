import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import re

class query_sparql():
    def __init__(self):
        self.baseEntity = "http://www.student-mat.com/entity/"
        self.baseProperty = "http://www.student-mat.com/pred/"
        self.endpoint = "http://localhost:7200"
        self.repo_name = "trabalho2"
        self.client = ApiClient(endpoint=self.endpoint)
        self.accessor = GraphDBApi(self.client)

    def list_all_triples(self):
        query = """
        PREFIX baseProperty: <http://www.student-mat.com/pred/>
        SELECT *
        WHERE{
            ?s?p?o

        }
        """
        payload_query = {"query": query}
        res = self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)
        res = json.loads(res)
        pattern = re.compile(".*http://www.student-mat.com/pred/.*")
        triples = []
        for e in res['results']['bindings']:
            if pattern.match(str(e['p']['value'])):
                sub = e['s']['value'].replace(self.baseEntity, '').title()
                pred = e['p']['value'].replace(self.baseProperty, '').title()
                obj = e['o']['value'].replace(self.baseEntity, '').title()
                triples.append((sub, pred, obj))
        return triples

    def add_sparql(self, sub, pred, obj):

        sub = sub.lower().replace(' ', '')
        pred = pred.lower().replace(' ', '')
        obj = obj.lower().replace(' ', '')
        if( pred == 'available'):
            update = """
                  PREFIX pred: <http://www.student-mat.com/pred/>
                  PREFIX entity: <http://www.student-mat.com/entity/>
                  INSERT DATA
                  {
                    entity:""" + sub + """ pred:""" + pred+""" entity:"""+ obj + """ .
                  }
              """
            payload_query = {"update": update}
            self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)
        else:
            update = """
                  PREFIX pred: <http://www.student-mat.com/pred/>
                  PREFIX entity: <http://www.student-mat.com/entity/>
                  INSERT DATA
                  {
                    entity:""" + sub + """ pred:""" + pred+""" \""""+ obj + """\" .
                  }
              """
            payload_query = {"update": update}
            self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)

    def rm_sparql(self, sub, pred, obj):
        if (str(sub) == '?s' and str(pred) == '?p'):
            update = """
                   PREFIX pred: <http://www.student-mat.com/pred/>
                   PREFIX entity: <http://www.student-mat.com/entity/>
                   DELETE
                   {?s ?p ?o} 
                   where
                   {
                       ?s ?p \"""" + obj + """\".
                       ?s ?p ?o
                   }
               """
            payload_query = {"update": update}
            self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)
        elif (str(obj) == '?o' and str(pred) == '?p'):
            update = """
                   PREFIX pred: <http://www.student-mat.com/pred/>
                   PREFIX entity: <http://www.student-mat.com/entity/>
                   DELETE
                   {?s ?p ?o} 
                   where
                   {
                       entity:""" + sub + """ ?p ?o.
                       ?s ?p ?o
                   }
               """
            payload_query = {"update": update}
            self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)

        elif (sub == '?s' and obj == '?o'):
            update = """
                   PREFIX pred: <http://www.student-mat.com/pred/>
                   PREFIX entity: <http://www.student-mat.com/entity/>
                   DELETE
                   {?s ?p ?o} 
                   where
                   {
                       ?s pred:""" + pred + """ ?o.
                       ?s ?p ?o
                   }
               """
            payload_query = {"update": update}
            self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)

        elif (str(sub) == '?s'):
            update = """
                   PREFIX pred: <http://www.student-mat.com/pred/>
                   PREFIX entity: <http://www.student-mat.com/entity/>
                   DELETE
                   {?s ?p ?o} 
                   where
                   {
                       ?s pred:""" + pred + """\"""" + obj + """\".
                       ?s ?p ?o
                   }
               """
            payload_query = {"update": update}
            self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)

        elif (str(pred) == '?p'):
            update = """
                   PREFIX pred: <http://www.student-mat.com/pred/>
                   PREFIX entity: <http://www.student-mat.com/entity/>
                   DELETE
                   {?s ?p ?o} 
                   where
                   {
                       entity:""" + sub + """ ?p \"""" + obj + """\".
                       ?s ?p ?o
                   }
               """
            payload_query = {"update": update}
            self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)

        elif (str(obj) == '?o'):

            update = """
                   PREFIX pred: <http://www.student-mat.com/pred/>
                   PREFIX entity: <http://www.student-mat.com/entity/>
                   DELETE
                   {?s ?p ?o} 
                   where
                   {
                       entity:""" + sub + """ pred:""" + pred + """ ?o .
                       ?s ?p ?o
                   }
               """
            payload_query = {"update": update}
            self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)

        else:

            space=" "
            update = """
                   PREFIX pred: <http://www.student-mat.com/pred/>
                   PREFIX entity: <http://www.student-mat.com/entity/>
                   DELETE where
                   {
                     entity:""" + sub + """ pred:""" + pred+""" \""""+ obj + """\" .
                   }
               """
            payload_query = {"update": update}
            self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)

    def triple_already_exists(self, sub, pred, obj=None):
        sub = sub.lower().replace(' ', '_')
        pred = pred.lower().replace(' ', '_')
        if obj is not None:
            obj = obj.lower().replace(' ', '_')
            query = """
                PREFIX pred: <http://www.student-mat.com/pred/>
                PREFIX entity: <http://www.student-mat.com/entity/>
                ASK
                {
                    entity:""" + sub + """ pred:""" + pred + """ entity:""" + obj + """ .
                } 
            """
        else:
            query = """
                PREFIX pred: <http://www.student-mat.com/pred/>
                PREFIX entity: <http://www.student-mat.com/entity/>
                ASK
                {
                    entity:""" + sub + """ pred:""" + pred + """ ?o """ + """ .
                } 
                """
        payload_query = {"query": query}
        res = self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)
        res = json.loads(res)

        return res['boolean']

    def get_all_predicates(self):
        triples = self.list_all_triples()
        predicates = []
        for sub, pred, obj in triples:
            if pred not in predicates:
                predicates.append(pred)
        return predicates

    def add_inferences(self, sub):
        space=" "
        for triple in sub.split(';'):
            if(triple!=""):
                triple = triple.split(' ')
                if len(triple) == 3 and triple[1] == 'available':

                    update = """
                                         PREFIX pred: <http://www.student-mat.com/pred/>
                                         PREFIX entity: <http://www.student-mat.com/entity/>
                                         INSERT DATA
                                         {
                                           entity:""" + triple[0] + """ pred:""" + triple[1] + space + """entity:"""+triple[2] + """ . 
                                         }
                                    """
                    payload_query = {"update": update}
                    res = self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)


                elif len(triple) == 3:
                    update = """
                         PREFIX pred: <http://www.student-mat.com/pred/>
                         PREFIX entity: <http://www.student-mat.com/entity/>
                         INSERT DATA
                         {
                           entity:""" + triple[0] + """ pred:""" + triple[1]+space+ """\""""+triple[2]+ """\"""" + """ . 
                         }
                    """
                    payload_query = {"update": update}
                    res=self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)

