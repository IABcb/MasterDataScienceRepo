#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 11:14:05 2016

@author: usuario
"""

import csv
from rdflib import Graph, Literal, URIRef, BNode

csvFile = open("/home/usuario/Escritorio/Transporte/Transporte.csv","r", encoding='latin-1')
csvReader = csv.reader(csvFile)

g = Graph()

adress = URIRef('http://dbpedia.org/ontology/adress')
code = URIRef('http://dbpedia.org/ontology/code')
parent = URIRef('http://dbpedia.org/ontology/parent')
name = URIRef('http://dbpedia.org/ontology/name')
order = URIRef('http://dbpedia.org/ontology/order')
tipo = URIRef('http://dbpedia.org/ontology/type')
isHandicappedAccessible = URIRef('http://dbpedia.org/ontology/isHandicappedAccessible')
location = URIRef('http://dbpedia.org/ontology/location')
timezone = URIRef('http://dbpedia.org/ontology/timezone')
line = URIRef('http://www.daml.org/ontologies/396#line')
homepage = URIRef('http://www.daml.org/ontologies/396#homepage')
lat = URIRef('http://www.w3.org/2003/01/geo/wgs84_pos#lat')
long = URIRef('http://www.w3.org/2003/01/geo/wgs84_pos#long')

for row in csvReader:
    g.add((BNode(row[3]), tipo, Literal(row[0])))
    g.add((BNode(row[3]), line, Literal(row[1])))
    g.add((BNode(row[3]), order, Literal(row[2])))
    g.add((BNode(row[3]), code, Literal(row[4])))
    g.add((BNode(row[3]), name, Literal(row[5])))
    g.add((BNode(row[3]), adress, Literal(row[6])))
    g.add((BNode(row[3]), lat, Literal(row[7])))
    g.add((BNode(row[3]), long, Literal(row[8])))
    g.add((BNode(row[3]), location, Literal(row[9])))
    g.add((BNode(row[3]), homepage, URIRef(row[10])))
    g.add((BNode(row[3]), parent, Literal(row[12])))
    g.add((BNode(row[3]), timezone, Literal(row[13])))
    g.add((BNode(row[3]), isHandicappedAccessible, Literal(row[14])))
    
g.serialize(destination ="Transporte.xml", format = "xml")