# Tong Zhao, tzhao2@nd.edu
# Paul Fortin, pfortin@nd.edu

import sys
from _product_sentiment_analysis import _product_sentiment_analysis

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