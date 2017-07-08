import re, os, numpy, string
import nltk
from sklearn.metrics.cluster import *
from sklearn.cluster import AgglomerativeClustering
from nltk.cluster import GAAClusterer
from sklearn.metrics.cluster import adjusted_rand_score
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import ngrams
from nltk.tag.stanford import StanfordNERTagger
from nltk.internals import find_jars_within_path

def read_file(file):
    myfile = open(file,"r")
    data = ""
    lines = myfile.readlines()
    for line in lines:
        data = data + line
    myfile.close
    return data

def cluster_texts(texts, clustersNumber, distance):
    #Load the list of texts into a TextCollection object.
    collection = nltk.TextCollection(texts)
    print("Created a collection of", len(collection), "terms.")

    #get a list of unique terms
    unique_terms = list(set(collection))
    print("Unique terms found: ", len(unique_terms))

    ### And here we actually call the function and create our array of vectors.
    vectors = [numpy.array(TF(f,unique_terms, collection)) for f in texts]
    print("Vectors created.")

    # initialize the clusterer
    clusterer = GAAClusterer(clustersNumber)
    clusters = clusterer.cluster(vectors, True)
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
    
    
stemmer = SnowballStemmer("english")
wordnet_lemmatizer = WordNetLemmatizer()

java_path = 'C:/Program Files (x86)/Java/jre1.8.0_101/bin/'
os.environ['JAVA_HOME'] = java_path
stanford_dir = 'C:/stanford-ner-2016-10-31/'
jarfile = stanford_dir + 'stanford-ner.jar'
modelfile = stanford_dir + 'classifiers/english.muc.7class.distsim.crf.ser.gz'
st = StanfordNERTagger(modelfile,jarfile)
stanford_jars = find_jars_within_path(stanford_dir)
st._stanford_jar = ';'.join(stanford_jars)


if __name__ == "__main__":
    folder = "Thomas_Baker"
    # Empty list to hold text documents.
    texts = []

    listing = os.listdir(folder)
    for file in sorted(listing):
        if file.endswith(".txt"):
            url = folder+"/"+file
            f = open(url,encoding="latin-1");
            raw = f.read()
            f.close()
            tokens = nltk.word_tokenize(raw)
            
            
            stop = set(stopwords.words('english'))
            filter_tokens = []
            for token in tokens:
                if token not in string.punctuation and stop:
                    filter_tokens.append(token) 
                    
                
            filtered_tokens = []
            for token in filter_tokens:
                if re.search('[a-zA-Z]', token):
                    filtered_tokens.append(token)
            
            ENs = []
            EN_words = st.tag(filtered_tokens) 
            for word in EN_words:
                if word[1] != 'O':
                    ENs.append(word[0])
             
            
            ngramas = []
            n = 3
            grams = ngrams(ENs,n)
            for gram in grams:
                ngramas.append(gram)
                            
            ngramas = list(set(ngramas))
            
             
            text = nltk.Text(ngramas)
            texts.append(text)

    print("Prepared ", len(texts), " documents...")
    print("They can be accessed using texts[0] - texts[" + str(len(texts)-1) + "]")

    distanceFunction ="cosine"
    #distanceFunction = "euclidean"
    test = cluster_texts(texts,4,distanceFunction)
    print("test: ", test)
    # Gold Standard
    reference =[0, 1, 2, 0, 0, 0, 3, 0, 0, 0, 2, 0, 3, 3, 0, 1, 2, 0, 1]
    print("reference: ", reference)

    # Evaluation
    print("rand_score: ", adjusted_rand_score(reference,test))

