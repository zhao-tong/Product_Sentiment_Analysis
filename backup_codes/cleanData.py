import re
import json
import preprocessor as pp

#Tong Zhao, tzhao2

def jaccardDistance(setA, setB):
    return len(setA.intersection(setB)) / len(setA.union(setB))

def getWords(string):
    return set(re.compile('\w+').findall(string))

if __name__ == '__main__':
    FILE_NAME = 'Note7_04'

    tweets = list()
    with open('rawdata/{}.json'.format(FILE_NAME), 'r') as f:
        for line in f:
            tweet = json.loads(line)
            tweets.append(tweet['text'])

    pp.set_options(pp.OPT.URL, pp.OPT.EMOJI)
    for i in range(len(tweets)):
        tweets[i] = pp.clean(tweets[i])

    label = [True] * len(tweets)

    for i in range(len(tweets)):
        if label[i]:
            set1 = getWords(tweets[i])
            for j in range(i + 1, len(tweets)):
                if label[j]:
                    set2 = getWords(tweets[j])
                    dis = jaccardDistance(set1, set2)
                    if dis > 0.85:
                        label[j] = False

    data = list()
    for i in range(len(tweets)):
        if label[i]:
            data.append(tweets[i])

    fw = open('cleaneddata/{}.txt'.format(FILE_NAME), 'w')
    #json.dump(data, fw)
    for line in data:
        fw.write('{}\n'.format(line))
    fw.close()
