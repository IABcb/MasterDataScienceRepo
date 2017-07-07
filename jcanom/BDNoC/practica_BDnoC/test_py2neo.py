import json
from py2neo import *
import xmltodict

graph = Graph(password="ratonera")
graph.begin()

# with open('sample2.json') as json_data:
#     doc = json.load(json_data)

print("Parsing XML")
with open('dblp.xml','r') as fd:
    doc = xmltodict.parse(fd.read())

print("Building graph")
for doc_type,docs in doc['dblp'].items():
    print("Adding " + str(doc_type))
    doc={}
    doc['type']=doc_type
    tipo = Node("Tipo",name=doc_type)
    graph.merge(tipo)
    total = len(docs)
    n_doc=1
    for i in docs:
        # i['key']=i['@key']
        # i['date']=i['@mdate']
        # i['type']=doc_type
        print(str(n_doc)+"/"+str(total))
        n_doc = n_doc + 1
        if 'title' in i and 'journal' in i and 'year' in i and 'author' in i:
            # print(type(i['title']))
            if isinstance(i['title'],str):
                paper = Node("Paper", title = i['title'],
                             journal=i['journal'], year = i['year'])
            else:
                print("Not added")
                pass

            graph.merge(paper)
            ab = Relationship(paper, "IS", tipo)
            graph.merge(ab)
            if isinstance(i['author'], list):
                for author in i['author']:
                    auth = Node("Author", name = author)
                    graph.merge(auth)
                    ab = Relationship(auth,"WRITES",paper)
                    graph.merge(ab)
            else:
                auth = Node("Author", name=i['author'])
                graph.merge(auth)
                ab = Relationship(auth, "WRITES", paper)
                graph.merge(ab)
        else:
            print("Not added")