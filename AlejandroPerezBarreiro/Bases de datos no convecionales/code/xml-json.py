# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 09:44:41 2017

@author: Alex
"""

import json
import time
from lxml import etree

context = etree.iterparse('dblp.xml', dtd_validation=True, events=("start", "end"))        
outfile = open('dblp.json', 'w') 

#Definimos el tipo de publicaciones que nos interesan    
types = set(['article', 'inproceedings', 'incollection'])
# Los tags disponibles son: author|editor|title|booktitle|pages|year|address|journal|volume|number|month|
#                           url|ee|cdrom|cite|publisher|note|crossref|isbn|series|school|chapter
childElements = set(["title", "booktitle", "year"]) #Tags que nos interesan

t0 = time.time()
paper = {} # Documento con los tags seleccionados
authors = []   # Lista de autores que escribieron el documento juntos
paperCounter = 0
for event, element in context:
    tag = element.tag
    if tag in childElements:
        if element.text:
            if tag == 'year':
                # Introducimos el año de publicacion como int
                paper[tag] = int(element.text)
            else:
                paper[tag] = element.text
        
    elif tag == "author":
        if element.text:
                authors.append(element.text)
    elif tag in types:
        paper["type"] = tag
    
        if event == 'end':
            paper['Authors'] = list(set(authors))
            print(paper)
            json.dump(paper, outfile)
        paperCounter += 1
        paperCounter
        paper = {}
        authors = []
        if paperCounter == 4000000:
            # Hay que poner el doble del numero que se quiera porque cuenta dos veces por publicacion
            break
        element.clear()
        while element.getprevious() is not None:
            del element.getparent()[0]
print("Introducidas {0} publicaciones validas in {1} s.".format(int(paperCounter/2), time.time()-t0))
outfile.close()
 
        