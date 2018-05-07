# Product Sentiment Analysis
Tong Zhao, tzhao2@nd.edu

Paul Fortin, pfortin@nd.edu

Course project for CSE60437 with Professor Dong Wang.

## Description
A tool to get the sentiment trend on Twitter for any inputed keyword. 

Note: the python version used for this product is 3.6.4.

## Components
- **API:** The API for this project.
- **Website:** A Django based webserver that utilized the API.
- **Backup:** All of our original codes before the API was built and all of the twitter data we used for this project.

## Examples of API usage in terminal
- Get the trend for keyword Trump for the last week.
``` 
python generater.py last_week Trump
```   

- Get the trend for keyword Trump for the last month.
``` 
python generater.py last_month Trump
``` 

- Get the trend for keyword Trump for the last *n* of *m*-day intervals.
``` 
python generater.py recent Trump m n
```   

- Get the trend for IphoneX for the one week prior its launch date and four weeks after its launch date.
``` 
python generater.py date IphoneX 2017-11-03
```   

- Run the website
```
python manage.py runserver
```

## Reference
-[GetOldTweets](https://github.com/Jefferson-Henrique/GetOldTweets-python)

-[VaderSentiment](https://github.com/cjhutto/vaderSentiment)

-[Preprocessor](https://pypi.org/project/tweet-preprocessor/)
