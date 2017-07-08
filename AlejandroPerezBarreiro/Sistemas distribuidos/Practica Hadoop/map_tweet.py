#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 13:46:08 2016

@author: usuario
"""

import sys
import json
import re, string

sys.path.append('./') #Añado el directorio actual

scores = json.load(open('diccionario.txt')) #Cargo el diccionario

for tweet in sys.stdin:
    tweetjson = json.loads(tweet)
    
    #Selecciono los tweets de Estados Unidos que tengan texto
    if 'text' in tweetjson and tweetjson['place']!=None and tweetjson['place'].get('country_code')=='US':
        location = tweetjson['place'].get('full_name')
        location = location.split(',')
        if len(location) == 2:
            key = location[1] #Asigno el estado a la clave

        #Calculo el valor del tweet
        tweetvalue = 0
        text = tweetjson['text']
        text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text) #Quito signos de puntuacion
        words = text.split()
        for w in words:
            if w in scores:
                tweetvalue += scores[w]
            else:
                tweetvalue += 0
            print('{0}\t{1}'.format(key,tweetvalue)) #Emito clave-valor


    
    
    
    
    
    
    
    
    
    
