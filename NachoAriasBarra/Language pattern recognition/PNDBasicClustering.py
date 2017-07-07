import re, pprint, os, numpy
# -*- coding: utf-8 -*-
import nltk
import string
path_to_append = '/media/nacho/f8371289-0f00-4406-89db-d575f3cdb35e/Master/Trimestre 2/RIM/nltk_data'
nltk.data.path.append(path_to_append)
from sklearn.metrics.cluster import *
from sklearn.cluster import AgglomerativeClustering
from nltk.cluster import GAAClusterer
from sklearn.metrics.cluster import adjusted_rand_score

def read_file(file):
    myfile = open(file,"r")
    data = ""
    lines = myfile.readlines()
    for line in lines:
        data = data + line
    myfile.close
    return data

def cluster_texts(texts, clustersNumber, distance):
    # Convierte texto en una coleccion
    # Load the list of texts into a TextCollection object.
    collection = nltk.TextCollection(texts)
    print("Created a collection of", len(collection), "terms.")

    # Para representar los textos como vectores de terminos representativos, cojo los terminos unicos
    # Get a list of unique terms
    unique_terms = list(set(collection))
    print("Unique terms found: ", len(unique_terms))

    ### And here we actually call the function and create our array of vectors.
    # TF mide la frecuencia en los textos.
    # Mira de los terminos unicos, cuantas veces aparece en el documento. No mira cuantas veces aparece en la coleccion
    # Hay otras medidas, como TF-IDF que son mas precisas porque tambien miran cuantas veces aparece en la coleccion
    vectors = [numpy.array(TF(f,unique_terms, collection)) for f in texts]
    print("Vectors created.")
    print(vectors)

    # initialize the clusterer
    clusterer = GAAClusterer(clustersNumber)
    clusters = clusterer.cluster(vectors, True)
    # Estas lineas siguientes comentadas es lo mismo pero con otra libreria, la llamada scikit-learn
    #clusterer = AgglomerativeClustering(n_clusters=clustersNumber,
    #                                  linkage="average", affinity=distanceFunction)
    #clusters = clusterer.fit_predict(vectors)

    return clusters

# Function to create a TF vector for one document. For each of
# our unique words, we have a feature which is the tf for that word
# in the current document
def TF(document, unique_terms, collection):
    word_tf = []
    for word in unique_terms:
        word_tf.append(collection.tf(word, document))
    return word_tf

if __name__ == "__main__":
    folder = "Thomas_Baker"
    # Empty list to hold text documents.
    texts = []

    listing = os.listdir(folder)
    for file in listing:
        if file.endswith(".txt"):
            url = folder+"/"+file
            f = open(url,encoding="latin-1");
            raw = f.read()
            f.close()
            tokens = nltk.word_tokenize(raw)
            text = nltk.Text(tokens)
            texts.append(text)

    print("Prepared ", len(texts), " documents...")
    print("They can be accessed using texts[0] - texts[" + str(len(texts)-1) + "]")

    # medida de similitud de los vectores de palabras
    distanceFunction ="cosine"
    #distanceFunction = "euclidean"
    # el 4 es el numero de grupos en los que se van a agrupar los individuos.
    # Lo ideal seria usar uno que no sepamos a priori cuantos grupos
    # tiene que hacer
    priori_groups = 4
    print(texts[0])
    test = cluster_texts(texts,priori_groups,distanceFunction)
    print("test: ", test)
    # Gold Standard
    # el documento que meto el primero sera igual que los que esten en todos los ceros
    reference =[0, 1, 2, 0, 0, 0, 3, 0, 0, 0, 2, 0, 3, 3, 0, 1, 2, 0, 1]
    print("reference: ", reference)

    # Evaluation
    print("rand_score: ", adjusted_rand_score(reference,test))

# entidades, eliminando palabras vacias, eliminar el nombre de la persona en las paginas web, representacion en ngramas a nivel de palabras
# (trigramas es poner casa-perro-coche en las ocurrencias por texto), se puede hacer los ngramas con nltk y scikit-learn
# hacer steaming, v er contenido de las paginas web

# La memoria tiene que justificar lo que hacemos, ejemplo hemos hecho el eliminar stopwords y justificar porque ha ido bien o mal

# las paginas tienen que estar agrupadas con el individuo que corresponde.

