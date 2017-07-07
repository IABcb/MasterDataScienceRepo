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

# Import the data corresponding to the 4clusters.csv file
data_4_clusters = pd.read_csv('CSV_output/4clusters.csv')
data_4_clusters_AC = data_4_clusters.loc[data_4_clusters.clustering_mode == "AgglomerativeClustering"]
data_4_clusters_kmeans = data_4_clusters.loc[data_4_clusters.clustering_mode == "KMeans"]
data_4_clusters_MBKM = data_4_clusters.loc[data_4_clusters.clustering_mode == "MiniBatchKMeans"]

# Plot data corresponding to the 4clusters.csv file: KMeans
data_4_clusters_kmeans.rand_score = data_4_clusters_kmeans.rand_score.astype(float)
data_4_clusters_kmeans.cluster_split = data_4_clusters_kmeans.cluster_split.astype(float)
data_4_clusters_kmeans = data_4_clusters_kmeans.sort_values(by="rand_score")
ax_kmeans_4 = data_4_clusters_kmeans.plot(x='model', y='rand_score', kind='bar',
                             title='KMeans, nclusters = 4', legend = False)
ax_kmeans_4.set_xlabel("Transformation")
ax_kmeans_4.set_ylabel("rand_score")

# Plot data corresponding to the 4clusters.csv file: MiniBatchKMeans
data_4_clusters_MBKM.rand_score = data_4_clusters_MBKM.rand_score.astype(float)
data_4_clusters_MBKM.cluster_split = data_4_clusters_MBKM.cluster_split.astype(float)
data_4_clusters_MBKM = data_4_clusters_MBKM.sort_values(by="rand_score")
ax_MBKM_4 = data_4_clusters_MBKM.plot(x='model', y='rand_score', kind='bar',
                             title='MiniBatchKMeans, nclusters = 4', legend = False)
ax_MBKM_4.set_xlabel("Transformation")
ax_MBKM_4.set_ylabel("rand_score")

# Plot data corresponding to the 4clusters.csv file: AgglomerativeClustering
data_4_clusters_AC.rand_score = data_4_clusters_AC.rand_score.astype(float)
data_4_clusters_AC.cluster_split = data_4_clusters_AC.cluster_split.astype(float)
data_4_clusters_AC = data_4_clusters_AC.sort_values(by="rand_score")
ax_ac_4 = data_4_clusters_AC.plot(x='model', y='rand_score', kind='bar',
                             title='AgglomerativeClustering, nclusters = 4', legend = False)
ax_ac_4.set_xlabel("Transformation")
ax_ac_4.set_ylabel("rand_score")

list_data = []
index = []
fil_keys = {"real":"n_4", "best":"n_variable"}
comp_modes = data_n_clusters_AC.comparing_mode.unique()
for model in data_n_clusters_AC.model.unique():
    curr_data = {}
    for mode in comp_modes:
        value = data_n_clusters_AC[(data_n_clusters_AC["model"]==model)
                                   & (data_n_clusters_AC["comparing_mode"]==mode)]["rand_score"].values[0]
        curr_data[fil_keys[mode]] = value
    list_data.append(curr_data)
    index.append(model)

new_df = pd.DataFrame(list_data, index=index)

ax_AC_n = new_df.plot(kind="bar", title='AgglomerativeClustering, nclusters = variable')
ax_AC_n.set_xlabel("Transformation")
ax_AC_n.set_ylabel("rand_score")

