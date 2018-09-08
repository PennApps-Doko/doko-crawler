import tweepy
import threading
import json

auth = tweepy.OAuthHandler("YzB4VSFh5FuKp3VxbFF9fUGCo", "9DRWn8hqwmQwZZWU2PApzc0kHhHWbSthNeMWENz3SMxnER57Eg")
auth.set_access_token("635264195-rPU2p6hUnUPLoKeXGb7L6WEDUIky2VgJYrCnwNLZ", "5SFiMksNHSuwUQIScs9FEBQxomGvZ8IsoFaBf2pVv4Cr6")

api = tweepy.API(auth)

def crawl():
    threading.Timer(10.0, crawl).start()
    public_tweets = api.favorites("PennappsD", 1)
    json_list = []
    for tweet in public_tweets:
        data = {}
        data['name'] = tweet.place.name
        data['text'] = tweet.text
        json_data = json.dumps(data)
        json_list.append(json_data)
    print(json_list)


data = {}
data['key'] = 'value'
json_data = json.dumps(data)

crawl()