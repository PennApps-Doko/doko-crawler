import tweepy
import threading
import json
import uuid
import dbhelper
import time
from yelpapi import YelpAPI


with open("./config.js", 'r') as f:
    config = json.load(f)
auth = tweepy.OAuthHandler(config['twitter_header_a'], config['twitter_header_b'])
auth.set_access_token(config["twitter_token_a"], config["twitter_token_b"])

api = tweepy.API(auth, wait_on_rate_limit=True)
yelp = YelpAPI(config['yelp'])

def crawl():
    threading.Timer(30.0, crawl).start()
    public_tweets = api.favorites("PennappsD", 1)
    json_list = []
    for tweet in public_tweets:
        texts = tweet.text.split(" ")
        ts = dbhelper.getData("Posts", {"content.url": texts[-1]})

        if tweet.place and len(ts) == 0:
            data = {}
            data['name'] = tweet.place.name
            data['content'] = {'text': "".join(texts[0:len(texts)-1]),
                               'images': [],
                               'source': "Twitter",
                               'url': texts[-1]}
            data['id'] = str(uuid.uuid1())
            data['time'] = time.time()
            for m in tweet.entities['media']:
                data['content']['images'].append(m["media_url_https"])

            res_spots = dbhelper.getData('Spots', {"name": data['name']})

            if res_spots.__len__() == 0:
                data['spotId'] = str(uuid.uuid1())
                coords = tweet.place.bounding_box.coordinates[0][0]

                if not coords:
                    coords = {
                        "lon": -75.192110,
                        "lat": 39.953321
                    }
                spot = {
                        "id": data['spotId'],
                        "name": data['name'],
                        "location": {"lon": coords[0],
                                     "lat": coords[1]}
                        }

                data['location'] = {"lon": coords[0], "lat": coords[1]}
                print('spot', spot)

                res_restaurant = dbhelper.getData("Restaurants", {"name": spot['name']})
                if res_restaurant.__len__() == 0:
                    print("rest")
                    spot['restaurantId'] = str(uuid.uuid1())
                    search = yelp.search_query(term=data['name'], longitude=spot['location']['lon'], latitude=spot['location']['lat'])
                    description = yelp.business_query(search['business'][0]['id'])
                    print('description', description)
                    rate = 4
                    url = "https://www.upenn.edu/"
                    tags =  ['fast-food', 'very-cheap', 'take-out', 'high-calorie']
                    if len(search['businesses']) > 0:
                        s = search['businesses'][0]
                        rate = s['rating']
                        url = s['url']
                        tags = []
                        for t in s['categories']:
                            tags.append(list(t.values())[0])
                    restaurant = {
                        "name": spot['name'],
                        "id": spot['restaurantId'],
                        "description": "It is a very well known fast food restaurant",
                        "rank": int(rate*2),
                        "url": url,
                        "tags": tags,
                        "price": description['price'],
                        "rating": description['rating']
                    }
                    dbhelper.setData("Restaurants", restaurant)
                    print('restaurant', restaurant)
                print('spot1', spot)
                dbhelper.setData("Spots", spot)
            else:
                for r in res_spots:
                    data['spotId'] = r['id']

            dbhelper.setData('Posts', data)
            print(data)


data = {}
data['key'] = 'value'
json_data = json.dumps(data)

crawl()
