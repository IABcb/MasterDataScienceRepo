#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 12:20:34 2016

@author: usuario
"""

from bs4 import BeautifulSoup
import requests, re
import csv

csvFile = open('lineasTranvia.csv','wt')
writer = csv.writer(csvFile)

def getLinks(pageUrl):
    html = requests.get("http://www.crtm.es/"+pageUrl)
    bsObj = BeautifulSoup(html.text, "html.parser")
    return bsObj.find("div", {"id":"contenido"}).findAll("a", 
                      href=re.compile("^(/tu-transporte-publico/metro-ligero/lineas/10__)((?!:).)*$"))
    
def getParadas(Url):
    html = requests.get("http://www.crtm.es/"+Url)
    bsObj = BeautifulSoup(html.text, "html.parser")
    return bsObj.find("tbody").findAll("a", 
                      href=re.compile("^(/tu-transporte-publico/metro-ligero/estaciones/10_)((?!:).)*$"))
    
    
links = getLinks("/tu-transporte-publico/metro-ligero/lineas.aspx")
for link in links:
    num = link.attrs["title"][6]
    paradas = getParadas(link.attrs['href'])
    count = 1
    for parada in paradas:
        param1 = ["ML",num,'{0}_{1}'.format(num,count),parada.get_text()]
        count += 1
        writer.writerow(param1)
        
csvFile.close()

def normaliza(cadena):
    from unicodedata import normalize, category
    return ''.join([x for x in normalize('NFD', cadena) if category(x) == 'Ll'])
    
csvFile = open('Tranvia.csv','wt')
writer = csv.writer(csvFile)


reader = csv.reader(open('lineasTranvia.csv', 'r'))
for row in enumerate(reader):
    reader1 = csv.reader(open('stopsTranvia.csv', 'r'))
    for row1 in enumerate(reader1):
        if normaliza(row[1][3].lower()) == normaliza(row1[1][2].lower()):
            param = row[1][:3] + row1[1]
            writer.writerow(param)
            
csvFile.close()
