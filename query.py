import tweepy
import threading
import json
import uuid
import dbhelper

with open("./config.js", 'r') as f:
    config = json.load(f)
auth = tweepy.OAuthHandler(config['twitter_header_a'], config['twitter_header_b'])
auth.set_access_token(config["twitter_token_a"], config["twitter_token_b"])

api = tweepy.API(auth)

def crawl():
    threading.Timer(10.0, crawl).start()
    public_tweets = api.favorites("PennappsD", 1)
    json_list = []
    for tweet in public_tweets:
        if tweet.place:
            data = {}
            data['name'] = tweet.place.name
            data['text'] = tweet.text
            data['images'] = []
            data['source'] = "Twitter"
            data['url'] = data['text'].split(" ")[-1]
            data['id'] = str(uuid.uuid1())
            for m in tweet.entities['media']:
                data['images'].append(m["media_url_https"])

            res_spots = dbhelper.getData('Spots', {"name": data['name']})

            if res_spots.__len__() == 0:
                data['spotId'] = str(uuid.uuid1())

                spot = {"id": data['spotId'],
                        "description": "This is the best food forever!",
                        "tags":"take-out",
                        "rank": 6,
                        "url": "https://www.upenn.edu/"}

                dbhelper.setData("spots", spot)
            else:
                for r in res_spots:
                    data['spotId'] = r['id']


            json_data = json.dumps(data)
            json_list.append(json_data)
    print(json_list)


data = {}
data['key'] = 'value'
json_data = json.dumps(data)

crawl()