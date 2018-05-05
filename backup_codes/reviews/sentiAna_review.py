# Tong Zhao, tzhao2

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import glob
import numpy as np

def main():
    analyzer = SentimentIntensityAnalyzer()
    scores = list()
    with open('s9.txt', 'r') as fr:
        for line in fr:
            s = analyzer.polarity_scores(line)['compound']
            if s != 0:
                scores.append(s)
    result = sum(scores) / len(scores)

    print(result)


if __name__ == '__main__':
    main()
