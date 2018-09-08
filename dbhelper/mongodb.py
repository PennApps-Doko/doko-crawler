import pymongo
import json


def build_connection():
    with open("./config.js", 'r') as f:
        db_config = json.load(f)["mongo"]

    myclient = pymongo.MongoClient(db_config)
    return myclient['doko']


def setData(collection, data):
    col = build_connection()[collection]
    if type(data) == type(list()):
        col.insert_many(data)
    else:
        col.insert_one(data)


def getData(collection, search_object):
    col = build_connection()[collection]
    data = col.find(search_object)
    res = []
    for i in data:
        res.append(i)
    return res
