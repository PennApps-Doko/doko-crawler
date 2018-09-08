import tweepy
import threading
import json
import uuid
import dbhelper
from yelpapi import YelpAPI


with open("./config.js", 'r') as f:
    config = json.load(f)
auth = tweepy.OAuthHandler(config['twitter_header_a'], config['twitter_header_b'])
auth.set_access_token(config["twitter_token_a"], config["twitter_token_b"])

api = tweepy.API(auth)
yelp = YelpAPI(config['yelp'])

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
                print(tweet.place.bounding_box.coordinates[0][0])
                spot = {
                        "id": data['spotId'],
                        "name": data['name'],
                        "location": {"lat": tweet.place.bounding_box.coordinates[0][0][0],
                                     "lon": tweet.place.bounding_box.coordinates[0][0][1]}
                        }
                res_restaurant = dbhelper.getData("Restaurant", {"name": spot['name']})
                if res_restaurant.__len__() == 0:
                    spot['restaurantId'] = str(uuid.uuid1())
                    search = yelp.search_query(term=data['name'], longitude=spot['location']['lon'], latitude=spot['location']['lat'])
                    rate = 8
                    url = "https://www.upenn.edu/"
                    tags =  ['fast-food', 'very-cheap', 'take-out', 'high-calorie']
                    if len(search['businesses']) > 0:
                        s = search['businesses'][0]
                        rate = s['rating']
                        url = s['url']
                        tags = []
                        for t in s['categories']:
                            tags.append(list(t.values())[0])
                    restrurant = {
                        "name": spot['name'],
                        "id": spot['restaurantId'],
                        "description": "It is a very well known fast food restaurant",
                        "rank": rate,
                        "url": url,
                        "tags": tags
                    }
                    dbhelper.setData("Restaurant", restrurant)
                dbhelper.setData("Spots", spot)
            else:
                for r in res_spots:
                    data['spotId'] = r['id']

            dbhelper.setData('Post', data)
            print(data)


data = {}
data['key'] = 'value'
json_data = json.dumps(data)

crawl()