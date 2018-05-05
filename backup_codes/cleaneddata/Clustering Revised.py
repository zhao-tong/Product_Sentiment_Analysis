# Author: Paul Fortin
#Twitter Clustering using sklearn k-means clustering
#Based on tutorial from : https://pythonprogramminglanguage.com/kmeans-text-clustering/

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import json

#import the dataset as a list of tweets. 
dataset = list()
with open('S8_01.txt') as data:
    for line in data:
        dataset.append(str(line))
#Get text of tweets
documents = list()
for tweet in dataset:
    documents.append(tweet4)

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


print("\n")
print("Prediction")

Y = vectorizer.transform(["chrome browser to open."])
prediction = model.predict(Y)
print(prediction)

Y = vectorizer.transform(["My cat is hungry."])
prediction = model.predict(Y)
print(prediction)
