# -*- coding: utf-8 -*-
# Importing libraries
import re, pprint, os, numpy
import nltk
from nltk import ngrams
#import goslate
from nltk.collocations import *
import string
from nltk.corpus import stopwords
path_to_append = '/media/nacho/f8371289-0f00-4406-89db-d575f3cdb35e/Master/Trimestre 2/RIM/nltk_data'
path_to_append = '/media/raul/Data/nltk_data'
path_to_append = '/home/raul/nltk_data'
nltk.data.path.append(path_to_append)
from sklearn.metrics.cluster import *
from sklearn.cluster import AgglomerativeClustering, KMeans, MiniBatchKMeans
from nltk.cluster import GAAClusterer
from sklearn.metrics.cluster import adjusted_rand_score
from nltk.corpus import stopwords
import operator
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import warnings
warnings.filterwarnings('ignore')
from nltk.tag import StanfordNERTagger
from nltk.stem.porter import PorterStemmer
from nltk.stem import SnowballStemmer
import csv
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
# %matplotlib inline


def read_file(file):
    """
    Function to read a file, whose path is specified by
    the input "file".
    """
    myfile = open(file, "r")
    data = ""
    lines = myfile.readlines()
    for line in lines:
        data = data + line
    myfile.close
    return data


def TF(document, unique_terms, collection):
    """
    Function to create a TF vector for one document which belongs to
    to a collection. For each of our unique words, we have a feature
    which is the tf for that word in the current document. The
    following imputs must be specified:
        *) document: the document to study
        *) collection: collection to which that document belongs
        *) unique_terms: unique terms of the collection
    """
    word_tf = []
    for word in unique_terms:
        word_tf.append(collection.tf(word, document))
    return word_tf


def cluster_texts(texts, clustersNumber, distanceFunction, clusterMode):
    """
    Function to cluster several texts. The following inputs must be
    specified:
        *) texts: collection of texts to cluster
        *) clustersNumber: number of clusters to be used
        *) distanceFunction: distance function to be used by the
           clustering algorithms
        *) clusterMode: cluster mode to be used:"AgglomerativeClustering",
           "KMeans" or "MiniBatchKMeans", all of them belonging to the
           scikit-learn library

    """

    collection = nltk.TextCollection(texts)
    # print("Created a collection of", len(collection), "terms.")

    # Get a list of unique terms
    unique_terms = list(set(collection))
    # print("Unique terms found: ", len(unique_terms))

    ### And here we actually call the function and create our array of vectors.
    # TF mide la frecuencia en los textos.
    # Mira de los terminos unicos, cuantas veces aparece en el documento. No mira cuantas veces aparece en la coleccion
    # Hay otras medidas, como TF-IDF que son mas precisas porque tambien miran cuantas veces aparece en la coleccion
    vectors = [numpy.array(TF(f, unique_terms, collection)) for f in texts]
    # print("Vectors created.")
    # print(vectors)

    # for vector in vectors:
    # print("Vector ", len(vector))

    # initialize the clusterer
    # clusterer = GAAClusterer(clustersNumber)
    # clusters = clusterer.cluster(vectors, True)
    # Estas lineas siguientes comentadas es lo mismo pero con otra libreria, la llamada scikit-learn

    if clusterMode == "AgglomerativeClustering":

        clusterer = AgglomerativeClustering(n_clusters=clustersNumber,
                                            linkage="average", affinity=distanceFunction)
        clusters = clusterer.fit_predict(vectors)

    elif clusterMode == "KMeans":

        clusterer = KMeans(n_clusters=clustersNumber, random_state=0)
        clusters = clusterer.fit(vectors).predict(vectors)

    elif clusterMode == "MiniBatchKMeans":

        clusterer = MiniBatchKMeans(n_clusters=clustersNumber, random_state=0)
        clusters = clusterer.fit(vectors).predict(vectors)
    else:
        print("Invalid cluster mode")
        return None

    return clusters

def get_language(possible_lan, text):
    """
    Function that returns the language of a text. The following
    inputs must be specified:
        *) text: text to be analyzed
        *) possible_lan: list of possible languages
            +) "EN":english
            +) "ES":spanish
    More info in: http://blog.alejandronolla.com/2013/05/15/detecting-text-language-with-python-and-nltk/
    """
    languages_score = {}
    for language in possible_lan:
        stopwords_set = set(stopwords.words(language))
        words_set = set(text)
        common_elements = words_set.intersection(stopwords_set)
        languages_score[possible_lan[language]] = len(common_elements)
    return max(languages_score.items(), key=operator.itemgetter(1))[0]


def delete_words_from_text(text, words_to_delete):
    """
    Function that filters a initial text excluding all
    the words specified in the list "words_to_delete"
    """
    words_to_include = []
    words_to_delete = [word.lower() for word in words_to_delete]

    for word in text:
        if word.lower() not in words_to_delete:
            words_to_include.append(word)

    return words_to_include


def get_named_entities_1(initial_document, selected_types):
    """
    Function that filters a initial document only including
    that words specified in the variable "selected_types".
    """
    named_entities = list()
    selected_entities = list()
    try:
        for sentence in initial_document:
            tokenized_sentence = nltk.word_tokenize(sentence)
            # tagged_sentence = nltk.pos_tag(tokenized_sentence)
            tagged_sentence = nltk.pos_tag(tokenized_sentence, tagset='universal')
            named_ent = nltk.ne_chunk(tagged_sentence, binary=False)
            named_entities.append(named_ent)

        for element in named_entities:
            word = element.pos()[0][0][0]
            type_word = element.pos()[0][0][1]
            if type_word in selected_types:
                selected_entities.append(word)

        return selected_entities

    except Exception as e:
        print(str(e))


def get_named_ent_txts_1(raw_texts):
    """
    Function that applies the function "get_named_entities_1"
    to a collection of texts "raw_texts"
    """
    named_ent_txts_1 = []
    for text in raw_texts:
        curr_named_ent = get_named_entities_1(text, types_included_1)
        text_to_append = nltk.Text(curr_named_ent)
        named_ent_txts_1.append(text_to_append)
    return named_ent_txts_1


def get_named_entities_2(initial_document):
    """
    Function that filters a document ("initial_document") only including
    the recognized named entities using the capabilities of
    the NLTK library.
    """
    named_entities = list()
    selected_entities = list()
    try:
        for sentence in initial_document:
            tokenized_sentence = nltk.word_tokenize(sentence)
            tagged_sentence = nltk.pos_tag(tokenized_sentence)
            #             tagged_sentence = nltk.pos_tag(tokenized_sentence, tagset= 'universal')
            named_ent = nltk.ne_chunk(tagged_sentence, binary=False)
            named_entities.append(named_ent)

        for element in named_entities:
            if hasattr(element[0], 'label') and element[0].label:
                selected_entities.append(element[0].leaves()[0][0])

        return selected_entities

    except Exception as e:
        print(str(e))


def get_named_ent_txts_2(raw_texts):
    """
    Function that applies the function "get_named_entities_2"
    to a collection of texts "raw_texts"
    """
    named_ent_txts_2 = []
    for text in raw_texts:
        curr_named_ent = get_named_entities_2(text)
        text_to_append = nltk.Text(curr_named_ent)
        named_ent_txts_2.append(text_to_append)
    return named_ent_txts_2


def get_entities_standorf(sample, types_named_entities):
    """
    Function that filters a document ("initial_document") only including
    the recognized named entities using the capabilities of
    the Stanford NER.
    """
    # Select the first classifier model
    stanford_classifier = os.environ.get('STANFORD_MODELS').split(':')[2]

    # Get the path for the StandorfNERTagger
    stanford_ner_path = os.environ.get('CLASSPATH').split(':')[0]

    st = StanfordNERTagger(stanford_classifier, stanford_ner_path, encoding='utf-8')
    result_named_entities = st.tag(sample.split())
    filtered_named_entities = []

    for item in result_named_entities:
        word, entity = item
        if entity in types_named_entities:
            #             filtered_named_entities.append((word, entity))
            filtered_named_entities.append(word)

    return filtered_named_entities


def get_named_ent_txts_3(raw_texts, types_named_entities):
    """
    Function that applies the function "get_entities_standorf"
    to a collection of texts "raw_texts"
    """
    named_ent_txts_3 = []
    for text in raw_texts:
        curr_named_ent = get_entities_standorf(text, types_named_entities)
        text_to_append = nltk.Text(curr_named_ent)
        named_ent_txts_3.append(text_to_append)
    return named_ent_txts_3

def get_texts_no_stop_words(raw_texts):
    """
    Function that deletes the stop words of a collection
    of texts included in the variable "raw_texts"
    """
    filtered_texts = []
    for text in raw_texts:
        language = {'en':'english', 'es':'spanish'}[get_language(possible_lan, text)]
        words_to_exclude = list(set(stopwords.words(language)))
        curr_filtered_text = delete_words_from_text(text, words_to_exclude)
        filtered_texts.append(nltk.Text(curr_filtered_text))
    return filtered_texts

def get_texts_exclude_tomas_baker(raw_texts):
    """
    Function that deletes the words "Thomas" and "Baker"
    of a collection of texts included in the variable "raw_texts"
    """
    filtered_texts = []
    for text in raw_texts:
        curr_filtered_text = delete_words_from_text(text, ['Thomas', 'Baker'])
        filtered_texts.append(nltk.Text(curr_filtered_text))
    return filtered_texts

def get_ngram(raw_texts, ngramlimit):
    ngramlist=[]
    for text in raw_texts:
        ngram_text = nltk.ngrams(text, ngramlimit)
        ngramlist.append(nltk.Text(ngram_text))
    return ngramlist


def stemming_2(text, lan='en'):
    """
    Function that "stems" a text.
    """
    stemmeds = []
    if lan == 'en':
        # Steamer ingles
        stemmer = PorterStemmer()
    elif lan == 'es':
        # Stemer espanol
        stemmer = SnowballStemmer("spanish")

    # Para cada token del texto obtenemos su raíz.
    for word in text:
        stemmed = stemmer.stem(word)
        stemmeds.append(stemmed)
    # Escribimos el resultado para compararlo con las palabras originales.
    return stemmeds


def get_stemmed_txts_2(raw_texts):
    """
    Function that applies the function "stemming_2"
    to a collection of texts "raw_texts"
    """
    stemmed_txts = []
    for text in raw_texts:
        language = get_language(possible_lan, text)
        stemmed_txt = stemming_2(text, language)
        text = nltk.Text(stemmed_txt)
        stemmed_txts.append(text)
    return stemmed_txts

def delete_repWords_stopWords(raw_texts):
    """
    Function that deletes the repeated words of
    all the texts included in the collection "raw_texts"
    """
    deleted_repeated = []
    for text in raw_texts:
        delete_repeated_texts = []
        text = [w.lower() for w in text]
        unique_terms = list(set(text))
#         print("Número de palabras del texto: ",str(len(text)))
#         print("Tamaño del vocabulario filtrado: ", str(len(unique_terms)))
        deleted_repeated.append(nltk.Text(unique_terms))
    return deleted_repeated


class SpanishLemmatizer():
    # Abrimos el fichero donde tenemos la información para cada palabra y lo cargamos en un diccionario.
    def __init__(self):
        with open('./Lemmatizer/lemmatization-es.txt', 'r', encoding="utf8") as f:
            self.lemma_dict = {}
            for line in f:
                if line.strip():  # Evitamos posibles líneas en blanco.
                    value, key = line.split(None, 1)  # Nos quedamos con los valores clave y valor.
                    # None implica espacio en blanco.
                    key = key.rstrip()  # Limpiamos la línea para evitar los caracteres de salto \n ó \r.
                    self.lemma_dict[key] = value
                    self.lemma_dict[value] = value  # Añadimos por si acaso también el valor como clave.

    # Obtenemos el lemma para la palabra solicitada si es que se dispone de él. En caso contrario devuelve la palabra.
    # Útil en los casos en los que no se haya aplicado un tratamiento previo del texto (stopwords y puntuación).
    def lemmatize(self, word):
        try:
            lemma = self.lemma_dict[word.lower()]
        except KeyError:
            lemma = word
        return lemma


def lemmatize_texts(raw_texts, possible_lan):
    nlemmas_texts = []
    for text in raw_texts:
        language = get_language(possible_lan, text)
        if language == 'en':
            # Seleccionamos el lematizador.
            wordnet_lemmatizer = WordNetLemmatizer()
            # Obtenemos los tokens de las sentencias.
            #             tokens = nltk.word_tokenize(text)

            lemmatizeds = []
            nlemmas = []

            for token in text:
                lemmatized = wordnet_lemmatizer.lemmatize(token)
                lemmatizeds.append(lemmatized)
                # print('token ',token)
                # print('lema ',lemmatized)
                # Obtenemos los lemmas consultando la base de datos de WordNet.
                list = wordnet.synsets(token)
                # Si encontramos alguna palabra relacionada obtenemos sus lemas y nos quedamos con el primero.
                if len(list) >= 1:
                    lemma = list[0].lemma_names('eng')
                    if len(lemma) > 1:
                        nlemmas.append(lemma[0])
                    else:
                        nlemmas.append((token))
                        # En caso contrario simplemente introducimos en la solución la palabra actual.
            else:
                nlemmas.append(token)
            nlemmas_texts.append(nltk.Text(nlemmas))
        elif language == 'es':
            lemmatizer = SpanishLemmatizer()

            # Obtenemos los tokens del texto.
            #             tokens = nltk.word_tokenize(text)
            nlemmas = []
            lemmatizeds = []
            for token in text:
                # Obtenemos los lemmas consultando el archivo de lemmas.
                lemmatized = lemmatizer.lemmatize(token)
                # print('token ',token)
                # print('lema ',lemmatized)
                lemmatizeds.append(lemmatized)
                # Obtenemos los lemmas consultando la base de datos de WordNet.
                list = wordnet.synsets(token, lang='spa')
                # Si encontramos alguna palabra relacionada obtenemos sus lemas y nos quedamos con el primero.
                if len(list) >= 1:
                    lemma = list[0].lemma_names('spa')
                    if len(lemma) >= 1:
                        nlemmas.append(lemma[0])
                    else:
                        nlemmas.append(token)
                # En caso contrario simplemente introducimos en la solución la palabra actual.
                else:
                    nlemmas.append(token)
            nlemmas_texts.append(nltk.Text(nlemmas))
        else:
            print('Lenguaje no reconocido')
    return nlemmas_texts


# Folder with all texts
folder = "Thomas_Baker"
# gsObj=goslate.Goslate()
types_named_entities = ["LOCATION", "PERSON", "ORGANIZATION"]
# Empty list to hold text documents.
raw_texts = []
raw_texts_2 = []
raw_texts_en = []
named_ent_txts_1 = []
types_included_1 = ['NOUN']

possible_lan = {"english": "en", "spanish": "es"}
clustering_modes = ["AgglomerativeClustering", "KMeans", "MiniBatchKMeans"]

# READ FILES
listing = os.listdir(folder)
for file in sorted(listing):
    if file.endswith(".txt"):
        url = folder + "/" + file
        print(file)
        f = open(url, encoding="latin-1");
        raw = f.read()
        f.close()
        f2 = open(url, 'r', encoding="utf8")
        raw2 = f2.read()
        f2.close()
        raw_texts_2.append(raw2)
        tokens = nltk.word_tokenize(raw)
        text = nltk.Text(tokens)
        raw_texts.append(text)

# TRANSFORMATIONS
print("Prepared ", len(raw_texts), " documents...")
print("They can be accessed using texts[0] - texts[" + str(len(raw_texts) - 1) + "]")

print('Using Stanford NER...')
stanford_ner_txts = get_named_ent_txts_3(raw_texts_2, types_named_entities)

print('Using Stanford NER removing Thomas Baker...')
stanford_ner_no_thomas_baker = get_texts_exclude_tomas_baker(stanford_ner_txts)

print("Removing non-stop words....")
texts_no_stop_words = get_texts_no_stop_words(raw_texts)

print("Removing Thomas Baker from the texts...")
texts_no_thomas_baker = get_texts_exclude_tomas_baker(raw_texts)

print("Getting text including only named entities according to criteria 1...")
named_ent_txts_1 = get_named_ent_txts_1(raw_texts)

print("Getting stemmed texts...")
stemmed_txts = get_stemmed_txts_2(raw_texts)

print("Getting no_tomas_stemmed...")
no_tomas_stemmed_txts = get_stemmed_txts_2(texts_no_thomas_baker)

print("Getting no_tomas_stemmed_no_stop...")
no_tomas_stemmed_no_stop_txts = get_texts_no_stop_words(no_tomas_stemmed_txts)

print("Getting no_tomas_stemmed_ent1...")
no_tomas_stemmed_ent1_txts = get_named_ent_txts_1(no_tomas_stemmed_txts)

print("Getting text including only named entities according to criteria 2...")
named_ent_txts_2 = get_named_ent_txts_2(raw_texts)

print("Getting text including only named entities according to criteria 2 and excluding the words 'Tomas' and 'Baker'")
named_ent_2_no_tomas_barker_txts = get_texts_exclude_tomas_baker(named_ent_txts_2)

print('Getting bigrams in texts')
bigrams_texts = get_ngram(raw_texts, 2)

print('Getting trigrams in texts')
trigrams_texts = get_ngram(raw_texts, 3)

print('Lemmatizing texts')
lemmatized_texts = lemmatize_texts(raw_texts, possible_lan)

print('Removing repeated words')
no_repeatedWords_noStopWords = delete_repWords_stopWords(raw_texts)

# Similarity distance
distanceFunction ="cosine"
# distanceFunction = "euclidean"

reference =[0, 1, 2, 0, 0, 0, 3, 0, 0, 0, 2, 0, 3, 3, 0, 1, 2, 0, 1]
print("reference: ", reference)

tested_models = {}
fix_grouping = 4
header_fields=['clustering_mode','model','rand_score','cluster_split']

# CLUSTERING, FIXED
csv_file = 'CSV_output/4clusters.csv'
with open(csv_file, 'w') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(header_fields)
    new_row = []

    for cluster_mode in clustering_modes:
        tested_models[cluster_mode] = {}
        tested_models[cluster_mode]["primitive"] = cluster_texts(raw_texts,fix_grouping,distanceFunction, cluster_mode)
        tested_models[cluster_mode]["identity_analysis_1"] = cluster_texts(named_ent_txts_1,fix_grouping,distanceFunction, cluster_mode)
        tested_models[cluster_mode]["stemmed_txts"] = cluster_texts(stemmed_txts,fix_grouping,distanceFunction, cluster_mode)
        tested_models[cluster_mode]["no_tomas_baker"] = cluster_texts(texts_no_thomas_baker,fix_grouping,distanceFunction, cluster_mode)
        tested_models[cluster_mode]["no_stop_words"] = cluster_texts(texts_no_stop_words,fix_grouping,distanceFunction, cluster_mode)
        tested_models[cluster_mode]["no_tomas_stemmed"] = cluster_texts(no_tomas_stemmed_txts,fix_grouping,distanceFunction, cluster_mode)
        tested_models[cluster_mode]["no_tomas_stemmed_no_stop"] = cluster_texts(no_tomas_stemmed_no_stop_txts,fix_grouping,
                                                                                distanceFunction, cluster_mode)
        tested_models[cluster_mode]["no_tomas_stemmed_ent1"] = cluster_texts(no_tomas_stemmed_ent1_txts,fix_grouping,distanceFunction,
                                                                             cluster_mode)
        tested_models[cluster_mode]["identity_analysis_2"] = cluster_texts(named_ent_txts_2,fix_grouping,distanceFunction, cluster_mode)
        tested_models[cluster_mode]["named_ent_2_no_tomas_barker"] = cluster_texts(named_ent_2_no_tomas_barker_txts,
                                                                 fix_grouping,distanceFunction, cluster_mode)
        tested_models[cluster_mode]['bigrams'] = cluster_texts(bigrams_texts,fix_grouping,distanceFunction, cluster_mode)
        tested_models[cluster_mode]['trigrams'] = cluster_texts(trigrams_texts, fix_grouping,distanceFunction, cluster_mode)
        tested_models[cluster_mode]['lemmatized'] = cluster_texts(lemmatized_texts, fix_grouping,distanceFunction, cluster_mode)
        tested_models[cluster_mode]['no_repeated_words'] = cluster_texts(no_repeatedWords_noStopWords,fix_grouping, distanceFunction, cluster_mode)
        tested_models[cluster_mode]['stanford_ner_txts'] = cluster_texts(stanford_ner_txts,fix_grouping,
                                                                         distanceFunction, cluster_mode)
        tested_models[cluster_mode]['stanford_ner_no_thomas_baker'] = cluster_texts(stanford_ner_no_thomas_baker,fix_grouping,
                                                                         distanceFunction, cluster_mode)

    # Evaluation
    tested_models_scores = {}

    for cluster_mode in tested_models:
        tested_models_scores[cluster_mode] = {}
        for model in tested_models[cluster_mode]:
            tested_models_scores[cluster_mode][model] = adjusted_rand_score(reference,tested_models[cluster_mode][model])
    #     print("Model ", model, "; rand_score = ", adjusted_rand_score(reference,tested_models[model]))

    for cluster_mode in tested_models_scores:
        print("**************************************")
        print("Getting results for the clustering mode ", cluster_mode)
        for model in sorted(tested_models_scores[cluster_mode].items(), key=operator.itemgetter(1), reverse=True):
            print("Model ", model[0], "; rand_score = ", model[1])
            new_row = [cluster_mode, model[0], model[1], fix_grouping]
            writer.writerow(new_row)
        print("########################################")
        print("########################################")


# CLUSTERING, CHANGING

tested_models = {}
top_cluster = 10
best_scores_all_clusters = {}
best_scores_Realcluster = {}
real_cluster_grouping = 4
init_scores = -999999
header_fields_compare = header_fields + ['comparing_mode']
csv_file = 'CSV_output/rangeclusters.csv'

with open(csv_file, 'a') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(header_fields)
    new_row = []

    for cluster_mode in clustering_modes:
        best_scores_all_clusters[cluster_mode] = {}
        best_scores_Realcluster[cluster_mode] = {}

    for cluster in range(1, top_cluster + 1):
        fix_grouping = cluster
        print('CLASIFICATION WITH ' + str(fix_grouping) + ' CLUSTERS')
        for cluster_mode in clustering_modes:
            tested_models[cluster_mode] = {}
            tested_models[cluster_mode]["primitive"] = cluster_texts(raw_texts, fix_grouping, distanceFunction,
                                                                     cluster_mode)
            tested_models[cluster_mode]["identity_analysis_1"] = cluster_texts(named_ent_txts_1, fix_grouping,
                                                                               distanceFunction, cluster_mode)
            tested_models[cluster_mode]["stemmed_txts"] = cluster_texts(stemmed_txts, fix_grouping, distanceFunction,
                                                                        cluster_mode)
            tested_models[cluster_mode]["no_tomas_baker"] = cluster_texts(texts_no_thomas_baker, fix_grouping,
                                                                          distanceFunction, cluster_mode)
            tested_models[cluster_mode]["no_stop_words"] = cluster_texts(texts_no_stop_words, fix_grouping,
                                                                         distanceFunction, cluster_mode)
            tested_models[cluster_mode]["no_tomas_stemmed"] = cluster_texts(no_tomas_stemmed_txts, fix_grouping,
                                                                            distanceFunction, cluster_mode)
            tested_models[cluster_mode]["no_tomas_stemmed_no_stop"] = cluster_texts(no_tomas_stemmed_no_stop_txts,
                                                                                    fix_grouping,
                                                                                    distanceFunction, cluster_mode)
            tested_models[cluster_mode]["no_tomas_stemmed_ent1"] = cluster_texts(no_tomas_stemmed_ent1_txts,
                                                                                 fix_grouping, distanceFunction,
                                                                                 cluster_mode)
            tested_models[cluster_mode]["identity_analysis_2"] = cluster_texts(named_ent_txts_2, fix_grouping,
                                                                               distanceFunction, cluster_mode)
            tested_models[cluster_mode]["named_ent_2_no_tomas_barker"] = cluster_texts(named_ent_2_no_tomas_barker_txts,
                                                                                       fix_grouping, distanceFunction,
                                                                                       cluster_mode)
            tested_models[cluster_mode]['bigrams'] = cluster_texts(bigrams_texts, fix_grouping, distanceFunction,
                                                                   cluster_mode)
            tested_models[cluster_mode]['trigrams'] = cluster_texts(trigrams_texts, fix_grouping, distanceFunction,
                                                                    cluster_mode)
            tested_models[cluster_mode]['lemmatized'] = cluster_texts(lemmatized_texts, fix_grouping, distanceFunction,
                                                                      cluster_mode)
            tested_models[cluster_mode]['no_repeated_words'] = cluster_texts(no_repeatedWords_noStopWords,
                                                                             fix_grouping, distanceFunction,
                                                                             cluster_mode)

            tested_models[cluster_mode]['stanford_ner_txts'] = cluster_texts(stanford_ner_txts, fix_grouping,
                                                                             distanceFunction, cluster_mode)
            tested_models[cluster_mode]['stanford_ner_no_thomas_baker'] = cluster_texts(stanford_ner_no_thomas_baker,
                                                                                        fix_grouping,
                                                                                        distanceFunction, cluster_mode)

        # Evaluation
        tested_models_scores = {}

        for cluster_mode in tested_models:
            tested_models_scores[cluster_mode] = {}
            for model in tested_models[cluster_mode]:
                tested_models_scores[cluster_mode][model] = adjusted_rand_score(reference,
                                                                                tested_models[cluster_mode][model])

                # Calculate the max score for each model, each custer amount
                if model in best_scores_all_clusters[cluster_mode].keys():
                    if best_scores_all_clusters[cluster_mode][model]['score'] <= tested_models_scores[cluster_mode][
                        model]:
                        best_scores_all_clusters[cluster_mode][model]['cluster'] = cluster
                        best_scores_all_clusters[cluster_mode][model]['score'] = tested_models_scores[cluster_mode][
                            model]
                else:
                    best_scores_all_clusters[cluster_mode][model] = {}
                    best_scores_all_clusters[cluster_mode][model]['cluster'] = cluster
                    best_scores_all_clusters[cluster_mode][model]['score'] = init_scores

                if cluster == real_cluster_grouping:
                    best_scores_Realcluster[cluster_mode][model] = {}
                    best_scores_Realcluster[cluster_mode][model]['cluster'] = cluster
                    best_scores_Realcluster[cluster_mode][model]['score'] = tested_models_scores[cluster_mode][model]

        for cluster_mode in tested_models_scores:
            print("**************************************")
            print("Getting results for the clustering mode ", cluster_mode)
            for model in sorted(tested_models_scores[cluster_mode].items(), key=operator.itemgetter(1), reverse=True):
                print("Model ", model[0], "; rand_score = ", model[1])
            print("########################################")
            print("########################################\n")

            new_row = [cluster_mode, model[0], model[1], cluster]
            writer.writerow(new_row)

csv_file = 'CSV_output/bestclusters.csv'
with  open(csv_file, 'a') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(header_fields_compare)
    new_row = []
    for cluster_mode in clustering_modes:
        print('/////////////////////////////////')
        print('CLUSTER ALGORITHM: ', cluster_mode)
        for model in best_scores_all_clusters[cluster_mode].keys():
            print('*Model: "', model, '". Best cluster agroupation: ',
                  best_scores_all_clusters[cluster_mode][model]['cluster'],
                  ' clusters. Score: ',
                  str(best_scores_all_clusters[cluster_mode][model]['score']))
            new_row = [cluster_mode, model,
                       best_scores_all_clusters[cluster_mode][model]['score'],
                       best_scores_all_clusters[cluster_mode][model]['cluster'], 'best']
            writer.writerow(new_row)

            print('++Score  for the real cluster agroupation (', str(real_cluster_grouping),
                  ') in model ', model, ' is ',
                  str(best_scores_Realcluster[cluster_mode][model]['score']))
            new_row = [cluster_mode, model,
                       str(best_scores_Realcluster[cluster_mode][model]['score']),
                       str(real_cluster_grouping), 'real']
            writer.writerow(new_row)
        print('/////////////////////////////////\n')



