# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 11:23:37 2017

@author: Alex
"""


import spotipy
import json
import networkx as nx
from networkx.readwrite import json_graph
import community


artist_name = 'melendi'
artistas = []
edges = []

sp = spotipy.Spotify()

melendi = sp.search(artist_name, type='artist')
artistas.append(melendi['artists']['items'][0])

result = sp.search(q='artist:' + artist_name, type='artist')

uri = result['artists']['items'][0]['uri']
target = 1
  
related = sp.artist_related_artists(uri)
for artist in related['artists']:
    source = 0
    edge = {}
    edge['source'] = source
    edge['target'] = target
    artistas.append(artist)
    edges.append(edge)
    source = target
    target = target + 1
                
      
    related1 = sp.artist_related_artists(artist['uri'])       
    for artista in related1['artists']:
        edge = {}
        edge['source'] = source
        edge['target'] = target
        artistas.append(artista)
        edges.append(edge)
        target = target + 1
 
       
data = {}
data['directed'] = False
data['graph'] = {}
data['nodes'] = artistas
data['links'] = edges
data['multigraph'] = False

with open('melendi.json', 'w') as outfile:
    json.dump(data, outfile)

#### Procesamiento NetworkX

g = json_graph.node_link_graph(data,multigraph=True, directed=False, attrs={'source': 'source', 'target': 'target', 'key': 'key', 'id': 'name'})

#Compruebo que es conexo (que por construccion se que si)
nx.node_connectivity(g)

# Detecto comunidades y se las añado a los artistas como propiedad
comunidades = community.best_partition(g)
for node in g.nodes():
    g.node[node]['community'] = comunidades[node]  
 
# Mido la importancia en el grafo en funcion a su grado
importances = nx.degree_centrality(g)
for node in g.nodes():
    g.node[node]['importance'] = importances[node]

g_json = json_graph.node_link_data(g)
with open('melendi_proces.json', 'w') as outfile:
    json.dump(g_json, outfile)

           
