import re, pprint, os, numpy

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.porter import PorterStemmer

from sklearn.metrics.cluster import *
from sklearn.cluster import AgglomerativeClustering
from nltk.cluster import GAAClusterer
from sklearn.metrics.cluster import adjusted_rand_score


def read_file(file):
    myfile = open(file, "r")
    data = ""
    lines = myfile.readlines()
    for line in lines:
        data = data + line
    myfile.close
    return data


def remove_stop_words(terms):
    filtered_terms = [term for term in terms if term not in stopwords.words('english')]
    return filtered_terms


def lemmatize(terms):
    lem_terms = list()
    wn_lem = WordNetLemmatizer()
    for term in terms:
        lem_terms.append(wn_lem.lemmatize(term, pos='v'))
    return lem_terms


def snow_stemming(terms):
    st_terms = list()
    stemmer = SnowballStemmer("english")
    for term in terms:
        st_terms.append(stemmer.stem(term))
    return st_terms


def lanc_stemming(terms):
    st_terms = list()
    stemmer = LancasterStemmer()
    for term in terms:
        st_terms.append(stemmer.stem(term))
    return st_terms


def porter_stemming(terms):
    st_terms = list()
    stemmer = PorterStemmer()
    for term in terms:
        st_terms.append(stemmer.stem(term))
    return st_terms

def pos_tagger(terms):
    tag_terms = nltk.pos_tag(terms)
    tag_terms = [term for term in tag_terms if term[1] in ["CD","JJ","JJR","JJS","MD","NN","NNP","NNPS","NNS",
                                                            "PDT","PRP","PRP$","RB","RBR","RBS","VB","VBD","VBG","VBN",
                                                            "VBP","VBZ"]]
    return tag_terms


def cluster_texts(texts, clustersNumber, distance):
    # Load the list of texts into a TextCollection object.
    collection = nltk.TextCollection(texts)
    print("Created a collection of", len(collection), "terms.")

    # get a list of unique terms
    unique_terms = list(set(collection))
    print("Unique terms found: ", len(unique_terms))

    # Removing "Thomas Baker" because it's a constant in every document
    print("Removing 'Thomas Baker'")
    unique_terms = [term for term in unique_terms if term not in ["thomas","baker"]]

    # Remove stopwords
    print("Removing stopwords")
    filtered_terms = remove_stop_words(unique_terms)
    print("Removed " + str(len(unique_terms) - len(filtered_terms)) + " terms")
    unique_terms = filtered_terms

    # Remove other "useless" words
    print("POS-tagging")
    pos_terms = pos_tagger(unique_terms)
    pos_terms = [term[0] for term in pos_terms]
    print("Removed " + str(len(unique_terms) - len(pos_terms)) + " terms")
    unique_terms = pos_terms

    # Lemmatization
    print("Lemmatization")
    lem_terms = lemmatize(unique_terms)
    collection = lemmatize(collection)
    # Removing posible duplicated lemmatized words
    print("Removed " + str(len(unique_terms) - len(list(set(lem_terms)))) + " terms")
    unique_terms = list(set(lem_terms))

    # # # Stemming
    # print("Stemming")
    # # st_terms = snow_stemming(unique_terms)
    # # st_terms = lanc_stemming(unique_terms)
    # st_terms = porter_stemming(unique_terms)
    # # collection = snow_stemming(collection)
    # # collection = lanc_stemming(collection)
    # collection = porter_stemming(collection)
    # print("Removed " + str(len(unique_terms) - len(list(set(st_terms)))) + " terms")
    # # Removing posible duplicated stemmed words
    # unique_terms = list(set(st_terms))

    print("Final unique terms: " + str(len(unique_terms)))

    collection = nltk.TextCollection(collection)

    ### And here we actually call the function and create our array of vectors.
    vectors = [numpy.array(TFIDF(lemmatize(f), unique_terms, collection)) for f in texts]
    print("Vectors created.")

    # # initialize the clusterer
    # clusterer = GAAClusterer(clustersNumber)
    # clusters = clusterer.cluster(vectors, True)

    clusterer = AgglomerativeClustering(n_clusters=clustersNumber,
                                     linkage="average", affinity=distanceFunction)
    clusters = clusterer.fit_predict(vectors)

    return clusters


# Function to create a TFIDF vector for one document. For each of
# our unique words, we have a feature which is the tf-idf for that word
# in the current document
def TFIDF(document, unique_terms, collection):
    word_tf = []
    for word in unique_terms:
        word_tf.append(collection.tf_idf(word, document))
    return word_tf

def TF(document, unique_terms, collection):
    word_tf = []
    for word in unique_terms:
        word_tf.append(collection.tf(word, document))
    return word_tf

if __name__ == "__main__":
    folder = "Thomas_Baker"
    # Empty list to hold text documents.
    texts = []

    listing = sorted(os.listdir(folder))
    for file in listing:
        if file.endswith(".txt"):
            # print("Reading "+file)
            url = folder + "/" + file
            f = open(url, encoding="latin-1");
            # Forcing lower case
            raw = f.read().lower()
            f.close()
            tokens = nltk.word_tokenize(raw)
            text = nltk.Text(tokens)
            texts.append(text)

    print("Prepared ", len(texts), " documents...")
    print("They can be accessed using texts[0] - texts[" + str(len(texts) - 1) + "]")

    distanceFunction = "cosine"
    # distanceFunction = "euclidean"
    test = cluster_texts(texts, 4, distanceFunction)
    print("test:\t\t", list(test))
    # Gold Standard
    reference = [0, 1, 2, 0, 0, 0, 3, 0, 0, 0, 2, 0, 3, 3, 0, 1, 2, 0, 1]
    print("reference:\t", reference)

    # Evaluation
    print("rand_score: ", adjusted_rand_score(reference, test))
