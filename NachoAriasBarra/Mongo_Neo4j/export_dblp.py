#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from pymongo import MongoClient
import sys

print("Dumping authors.csv")
file = codecs.open("authors.csv", "w", "utf-8")
# CSV header for 'Author' label
file.write (":ID\tname\n")
counter = 0
conex = MongoClient('localhost', 27017)
db = conex.docos
authors = db['authors']
cursor = authors.find({})
for doc in cursor:
    counter += 1
    if (counter % 10000 == 0) :
        sys.stdout.write("#")
        sys.stdout.flush()
    if (counter % 800000 == 0) :
        print('')
    if "'" in doc['name'] :
        file.write('"' + doc['_id'] + '"\t"' + doc['name'] + '"\n')
    else :
        file.write(doc['_id'] + '\t' + doc['name']+ '\n')

file.close()
print("\nDumped authors.csv\n")

print("Dumping publications.csv")
file = codecs.open("publications.csv", "w", "utf-8")
# CSV header for 'Publication' label
file.write(":ID\tcontainer\ttitle\ttype\tyear\n")
counter = 0
conex = MongoClient('localhost', 27017)
db = conex.docos
publications = db['publications']
cursor = publications.find({})
discards = []
for doc in cursor:
    counter += 1
    if counter%10000 == 0:
        sys.stdout.write("#")
        sys.stdout.flush()
    if counter%800000 == 0:
        print('')
    try:
        if "'" in doc['title']:
            file.write(doc['publication_id'] + '\t' +
                       doc['container'].replace("'", "").replace('"', '') +
                       '\t"' + doc['title'].replace('"', '') + '"\t' +
                       doc['type'] + '\t' +
                       str(doc['year']) + '\n')
        else:
            file.write(doc['publication_id'] + '\t' +
                       doc['container'].replace("'", "").replace('"', '') +
                       '\t' +  doc['title'].replace('"', '') + '\t' +
                       doc['type'] + '\t' +
                       str(doc['year']) + '\n')
    except Exception as e:
        if 'publication_id' in doc:
            discards.append(doc['publication_id'])

file.close()
print("\nDumped publications.csv\n")

print("Dumping relationships.csv")
file = codecs.open("relationships.csv", "w", "utf-8")
# CSV header for 'HAS_PUBLISHED' label
file.write (":START_ID\t:END_ID\n")
counter = 0
conex = MongoClient('localhost', 27017)
db = conex.docos
relationships = db['relationships']
cursor = relationships.find({})
for doc in cursor:
    counter += 1
    if (counter % 10000 == 0) :
        sys.stdout.write("#")
        sys.stdout.flush()
    if (counter % 800000 == 0) :
        print('')
    if doc['publication_id'] not in discards:
        if "'" in doc['name'] :
            file.write('"' + doc['name'] + '"\t' +
                       doc['publication_id'] + '\n')
        else :
            file.write(doc['name'] + '\t' +
                       doc['publication_id']+ '\n')

file.close()
print("\nDumped relationships.csv")
