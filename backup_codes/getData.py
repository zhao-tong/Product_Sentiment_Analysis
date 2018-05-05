import tweepy
import json

#Tong Zhao, tzhao2

def preset():
    consumer_key = 'Y39YTOi4e9cYsLrrdys7FmFmC'
    consumer_secret = 'pgBOQOIoZj6YAawvOFjNRCs5YLR7JZpvGRthbBSK9rxHB2wVpp'
    access_token = '595914367-U6PczRzl7v9u0HIfP9VGv39Zxz8t14XbiVusuOC8'
    access_token_secret = 'T7jL8KS3UCjKwwKej9D3byYd8bF42wbz1okTMxKgigP4y'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def search(keyword):
    api = preset()
    f = open('output.json','w')
    for tweet in tweepy.Cursor(api.search,
                                q=keyword,
                                rpp=100,
                                result_type="recent",
                                include_entities=True,
                                lang="en").items():
        tmp = {}
        tmp["time"] = str(tweet.created_at)
        tmp["text"] = tweet.text
        tmp["retweeted"] = tweet.retweeted
        json.dump(tmp, f)
        f.write('\n')
        #f.write('{0}\n'.format(str(tmp)))
    f.close()

if __name__ == '__main__':
    keyword = ['#Galaxy s9']
    search(keyword)
