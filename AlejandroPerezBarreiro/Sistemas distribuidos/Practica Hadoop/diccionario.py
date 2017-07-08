# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 11:08:50 2016

@author: Alex
"""

import json

file = open("C:\\Users\MSI\Desktop\Practica\AFINN-111.txt")
arch = open('diccionario.txt','w')
scores = {} # Inicio un diccionario vacio
for line in file:
    term, score = line.split("\t")
    scores[term] = int(score) 
    scores.items()
json.dump(scores, open("diccionario.txt",'w'))
arch.close()