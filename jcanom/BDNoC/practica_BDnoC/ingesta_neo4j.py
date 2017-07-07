import json
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "ratonera"))
session = driver.session()

with open('sample2.json') as json_data:
    doc = json.load(json_data)

for doc_type,docs in doc['dblp'].items():
    doc={}
    doc['type']=doc_type
    session.run("MERGE (a:PaperType {type: {type}})", doc)
    for i in docs:
        i['key']=i['@key']
        i['date']=i['@mdate']
        i['type']=doc_type
        session.run("MERGE (a:Paper {date: {date}, key: {key}, author: {author},"
                    "title: {title}, page: {pages}, year: {year}, volume: {volume},"
                    "journal: {journal}, url:{url}, ee:{ee}, type:{type}})",i)


session.run("MATCH (a: Paper),(b: PaperType {type:{type}})"
    "WHERE {type} = b.type"
    "CREATE (a)-[w:TIPO]-(b)"
    "RETURN w", i)


session.close()
