# Author: Paul Fortin
#Twitter Clustering using sklearn k-means clustering
#Based on tutorial from : https://pythonprogramminglanguage.com/kmeans-text-clustering/

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import numpy as np
import preprocessor as pp

import json

#https://stackoverflow.com/questions/36195457/python-sklearn-kmeans-how-to-get-the-values-in-the-cluster
def ClusterIndicesNumpy(clustNum, labels_array): #numpy
    return np.where(labels_array == clustNum)[0]

#import the dataset as a list of tweets.
dataset = list()
with open('Note7_all.json') as data:
    for line in data:
        dataset.append(json.loads(line.strip()))

#Get text of tweets
documents = list()
for tweet in dataset:
    documents.append(tweet['text'])

pp.set_options(pp.OPT.URL, pp.OPT.EMOJI)
for i in range(len(documents)):
    documents[i] = pp.clean(documents[i])

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

true_k = 25
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print

for x in range(0, true_k):
    index = ClusterIndicesNumpy(x, model.labels_)
    with open('note7_all/cluster{0}.txt'.format(x), 'w') as fw:
        for i in index:
            fw.write(documents[i])#.encode("ascii", errors='ignore').decode("ascii"))
            fw.write('\n')
