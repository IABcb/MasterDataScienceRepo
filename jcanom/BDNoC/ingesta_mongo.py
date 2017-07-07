import xmltodict
from pymongo import MongoClient
import json

print("Initializing mongo client")
client = MongoClient()

print("Parsing xml")
# with open('api_2017.xml','r') as fd:
with open('/media/javi/HDD2/BDNoSQL/dblp_1M.xml','r') as fd:
    doc = xmltodict.parse(fd.read())

# with open('sample.json') as json_data:
#     doc = json.load(json_data)

print("Setting mongo db and collection")
db = client.dblp2
dblp2 = db.dblp2

print("Dumping docs")
# for post in doc['result']['hits']['hit']:
for doc_type,docs in doc['dblp'].items():
    for i in docs:
        i['type'] = doc_type
    dblp2.insert_many(docs)

print("Done!")

