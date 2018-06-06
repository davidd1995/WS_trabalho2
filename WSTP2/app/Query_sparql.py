import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import re

class Query_sparl():
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

    def add_tosparl(self, sub, pred, obj):

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

    def rm_tosparl(self, sub, pred, obj):
        before_remove = len(self.list_all_triples())
        if sub is None:
            sub = '?s'
        else:
            sub = str('<' + self.baseEntity + sub + '>').lower().replace(' ', '')
        if obj is None:
            obj = '?o'
        if pred is None:
            pred = '?p'
        else:
            pred = str('<' + self.baseProperty + pred + '>').lower().replace(' ', '')
        print(sub+" "+pred+" "+obj)
        update = """
        DELETE DATA
           {
               entity:""" + sub + """ pred:""" + pred + """ """ + obj + """ .
           }
        """
        payload_query = {"update": update}
        self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)
        after_remove = len(self.list_all_triples())
        return before_remove - after_remove

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
        print(predicates)
        return predicates

    def add_inferences(self, sub):
        space=" "
        for triple in sub.split(';'):
            if(triple!=""):
                triple = triple.split(' ')
                if len(triple) == 3 and triple[1] == 'available':
                    print("boupa3")
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
                    print(res)
