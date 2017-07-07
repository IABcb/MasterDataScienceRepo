#!/usr/bin/env python
import urllib
import urllib2
import sys
import json
import unicodedata
import re
import csv

opener = urllib.URLopener()
# Dirección donde está almacenado el diccionario de sentimientos
csvFile = opener.open('https://s3-eu-west-1.amazonaws.com/urjc.datascience.jcano/tweets/Redondo_words_comas.csv')
# Leemos el diccionario de sentimientos
palabras = csv.DictReader(csvFile,fieldnames=['key','value'])
# URL del servidor de geolocalización inversa (MODIFICAR ANTES DE LANZAR)
url = 'http://54.171.111.87:2322/reverse'

# Función para eliminar las tildes
def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    return s.decode()
    
# Función para eliminar números y símbolos
def solo_letras ( text ):
    regex = re.compile('[^a-zA-Z]')
    return regex.sub('',text)

reload(sys)
sys.setdefaultencoding('utf8')

# Limpiamos las palabras del fichero de sentimientos y creamos un diccionario
sentimientos = {}
for p in palabras:
    p['key'] = elimina_tildes(p['key'])
    sentimientos[p['key']] = p['value']

# Se lee una línea de STDIN (Entrada de los Tweets)
for line in sys.stdin:
    # Cambiamos el encoding del Tweet
    line = line.encode('utf8')
    try:
        record = json.loads(line,encoding='latin-1')
    except ValueError:
        pass
    # Comprobamos que el lenguaje del Tweet es español
    if record["lang"]=="es":
        # Guardamos el texto
        line = record["text"]
        # Guardamos las coordenadas
        coords = record["coordinates"]
        if coords is not None:
            lon = str(coords["coordinates"][0])
            lat = str(coords["coordinates"][1])
            values = {'lon' : lon, 'lat' : lat}
            data = urllib.urlencode(values)
            full_url = url + '?' + data
            # Hacemos una petición de geolocalización inversa
            response = urllib2.urlopen(full_url)
            # Leemos la respuesta
            location_raw = response.read()
            location = json.loads(location_raw)
            # Extraemos el código postal (key)
            try:
                cp = location['features'][0]['properties']['postcode']
            except KeyError:
                continue

            # Obtenemos la valoración de las palabras del Tweet actual (value)
            words = line.split()
            valoracion = 0
            for word in words:  
                word = elimina_tildes(word)  
                word = solo_letras(word)
                if sentimientos.has_key(word):
                    valoracion = valoracion+float(sentimientos[word])

            # Emitimos el par <key,value> para que lo analice el reducer
            print '{0}\t{1}'.format(cp,valoracion)
                
