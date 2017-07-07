import xmltodict
from pymongo import MongoClient
import json

print("Initializing mongo client")
client = MongoClient()

print("Parsing xml")
# with open('api_2017.xml','r') as fd:
with open('dblp.xml','r') as fd:
    doc = xmltodict.parse(fd.read())

# with open('sample.json') as json_data:
#     doc = json.load(json_data)

print("Setting mongo db and collection")
db = client.dblp
dblp = db.dblp

print("Dumping docs")
# for post in doc['result']['hits']['hit']:
for doc_type,docs in doc['dblp'].items():
    for i in docs:
        i['type'] = doc_type
    dblp.insert_many(docs)

print("Done!")
