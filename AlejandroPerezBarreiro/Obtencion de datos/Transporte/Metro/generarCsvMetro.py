#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 20:35:40 2016

@author: usuario
"""

from bs4 import BeautifulSoup
import requests, re
import csv

csvFile = open('lineasMetro.csv','wt')
writer = csv.writer(csvFile)

def getLinks(pageUrl):
    html = requests.get("http://www.crtm.es/"+pageUrl)
    bsObj = BeautifulSoup(html.text, "html.parser")
    return bsObj.find("div", {"id":"contenido"}).findAll("a", 
                      href=re.compile("^(/tu-transporte-publico/metro/lineas/4__)((?!:).)*$"))
    
def getParadas(Url):
    html = requests.get("http://www.crtm.es/"+Url)
    bsObj = BeautifulSoup(html.text, "html.parser")
    return bsObj.find("tbody").findAll("a", 
                      href=re.compile("^(/tu-transporte-publico/metro/estaciones/4_)((?!:).)*$"))
    
    
links = getLinks("/tu-transporte-publico/metro/lineas.aspx")
for link in links:
    num = link.attrs["title"][6:8]
    paradas = getParadas(link.attrs['href'])
    count = 1
    for parada in paradas:
        if parada.get_text() != '\xa0':
            param1 = ["METRO",num,'{0}_{1}'.format(num,count),parada.get_text()]
            count += 1
            writer.writerow(param1)
        
csvFile.close()

def normaliza(cadena):
    from unicodedata import normalize, category
    return ''.join([x for x in normalize('NFD', cadena) if category(x) == 'Ll'])
    
csvFile = open('Metro.csv','wt')
writer = csv.writer(csvFile)


reader = csv.reader(open('lineasMetro.csv', 'r'))
for row in enumerate(reader):
    reader1 = csv.reader(open('stopsMetro.csv', 'r'))
    for row1 in enumerate(reader1):
        if normaliza(row[1][3].lower()) == normaliza(row1[1][2].lower()):
            param = row[1][:3] + row1[1]
            writer.writerow(param)
            
csvFile.close()