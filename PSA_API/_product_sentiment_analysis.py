# Tong Zhao, tzhao2@nd.edu
# Paul Fortin, pfortin@nd.edu

import os
import sys
import glob
import json
import codecs
import got3 as got
import numpy as np
import preprocessor as pp
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import date, datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
__version__ = '0.0.1'

class _product_sentiment_analysis:
    """docstring for _product_sentiment_analysis"""
    def __init__(self, keyword, date=date.today(), keyword2=None, date2=None):
        self.keyword = keyword
        self.date = date
        self.keyword2 = keyword2
        self.date2 = date2

    def jaccardDistance(self, setA, setB):
        return len(setA.intersection(setB)) / len(setA.union(setB))

    def getData(self, filename, start_time, end_time, num):
        tweetCriteria = got.manager.TweetCriteria()
        tweetCriteria.querySearch = self.keyword
        tweetCriteria.since = start_time
        tweetCriteria.until = end_time
        tweetCriteria.maxTweets = num
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        outputFile = codecs.open('tmp/{}'.format(filename), "w+", "utf-8")
        #print(len(tweets))
        for t in tweets:
            tmp = {}
            tmp["time"] = t.date.strftime("%Y-%m-%d %H:%M")
            tmp["text"] = t.text
            tmp["retweeted"] = t.retweets
            json.dump(tmp, outputFile)
            outputFile.write('\n')
        outputFile.flush()

    def clusterIndicesNumpy(self, clustNum, labels_array):
        return np.where(labels_array == clustNum)[0]

    def cluster_data(self, filename):
        #import the dataset as a list of tweets.
        dataset = list()
        with open('tmp/{}'.format(filename)) as data:
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

        noise_clusters = list()
        order_centroids = model.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()
        for i in range(true_k):
            keys = list()
            for ind in order_centroids[i, :10]:
                keys.append(terms[ind])
            if 'giveaway' in keys or 'giveawayhttps' in keys:
                noise_clusters.append(i)

        for x in range(0, true_k):
            if x not in noise_clusters:
                index = self.clusterIndicesNumpy(x, model.labels_)
                with open('tmp/clusters/cluster{0}.txt'.format(x), 'w') as fw:
                    for i in index:
                        fw.write(documents[i])
                        fw.write('\n')

    def get_sentiment(self):
        path = 'tmp/clusters/'
        upper = 0
        totalN = 0
        analyzer = SentimentIntensityAnalyzer()
        for filename in glob.glob(os.path.join(path, 'cluster*.txt')):
            scores = list()
            with open(filename, 'r') as fr:
                for line in fr:
                    s = analyzer.polarity_scores(line)['compound']
                    scores.append(s)
            arr = np.array(scores)
            num = np.count_nonzero(arr)
            result = 0.0
            if num > 0:
                result = arr.sum() / num
                totalN += num
                upper += arr.sum()
            #print('{}, result: {}, #: {}'.format(filename, result, num))
        return upper / totalN

    def get_plot(self, x, y, title, x_label, y_label):
        f = plt.figure()
        plt.plot(x, y)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
        f.savefig('tmp.png')

    def get_last_week(self):
        one_day = timedelta(1)
        start_time = self.date
        x = list()
        y = list()
        for i in range(7):
            end_time = start_time + one_day
            self.getData('tmp.json', start_time.isoformat(), end_time.isoformat(), 2000)#5000)
            self.cluster_data('tmp.json')
            score = self.get_sentiment()
            x.insert(0, start_time.isoformat())
            y.insert(0, score)
            start_time = start_time - one_day
        title = 'Sentiment trend for {} in the last week'.format(self.keyword)
        self.get_plot(x, y, title, 'Date', 'Sentiment Score')

    def get_last_month(self):
        one_day = timedelta(3)
        start_time = self.date - one_day
        x = list()
        y = list()
        for i in range(10):
            end_time = start_time + one_day
            self.getData('tmp.json', start_time.isoformat(), end_time.isoformat(), 2000)
            self.cluster_data('tmp.json')
            score = self.get_sentiment()
            x.insert(0, start_time.isoformat())
            y.insert(0, score)
            start_time = start_time - one_day
        title = 'Sentiment trend for {} in the last week'.format(self.keyword)
        self.get_plot(x, y, title, 'Date', 'Sentiment Score')

    def get_recent(self, interval, length):
        days = timedelta(interval)
        start_time = self.date - days
        x = list()
        y = list()
        for i in range(length):
            end_time = start_time + days
            self.getData('tmp.json', start_time.isoformat(), end_time.isoformat(), 2000)
            self.cluster_data('tmp.json')
            score = self.get_sentiment()
            x.insert(0, end_time.isoformat())
            y.insert(0, score)
            start_time = start_time - days
        title = 'Sentiment trend for {} recently.'.format(self.keyword)
        self.get_plot(x, y, title, 'Date', 'Sentiment Score')

    def get_around_date(self):
        one_week = timedelta(7)
        x = list()
        y = list()
        start_time = self.date - one_week
        end_time = self.date
        for i in range(5):
            self.getData('tmp.json', start_time.isoformat(), end_time.isoformat(), 10000)
            self.cluster_data('tmp.json')
            score = self.get_sentiment()
            x.insert(0, 'Week {}'.format(i))
            y.insert(0, score)
            start_time = start_time + one_week
            end_time = end_time + one_week
        title = 'Sentiment trend for {0} around {1}'.format(self.keyword, self.date.isoformat())
        self.get_plot(x, y, title, 'Time', 'Sentiment Score')
        print('x', x)
        print('y', y)

def main():
    if len(sys.argv) < 3:
        print('To run this file: {0} <keyword> <function> <date(YYYY-MM-DD)>(optional)\n \
            Supported functions are: now, stream, date'.format(sys.argv[0]))
        exit(-1)
    
    if sys.argv[1] == 'last_week':
        psa = _product_sentiment_analysis(sys.argv[2])
        psa.get_last_week()
    elif sys.argv[1] == 'last_month':
        psa = _product_sentiment_analysis(sys.argv[2])
        psa.get_last_month()
    elif sys.argv[1] == 'recent':
        psa = _product_sentiment_analysis(sys.argv[2])
        interval = int(sys.argv[3])
        length = int(sys.argv[4])
        psa.get_recent(interval, length)
    elif sys.argv[1] == 'date':
        try:
            date = datetime.strptime(sys.argv[3], "%Y-%m-%d").date()
        except:
            print('Invalid time format, please use YYYY-MM-DD.')
            exit(-1)
        psa = _product_sentiment_analysis(sys.argv[2], date)
        psa.get_around_date()
    elif sys.argv[1] == 'comp':
        psa = _product_sentiment_analysis(sys.argv[2])
        #psa.get_stream()

if __name__ == '__main__':
    main()
