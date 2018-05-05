# Tong Zhao, tzhao2

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import glob
import numpy as np

PATH = 'rawdata/s9_all/'
#PATH = 'cleaneddata/'

def main():
    upper = 0
    totalN = 0
    analyzer = SentimentIntensityAnalyzer()
    for filename in glob.glob(os.path.join(PATH, 'cluster*.txt')):
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

        print('{}, result: {}, #: {}'.format(filename, result, num))
    print(upper/totalN)


if __name__ == '__main__':
    main()
