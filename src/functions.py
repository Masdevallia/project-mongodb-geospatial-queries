
from pymongo import MongoClient
import pandas as pd
import numpy as np
import requests


def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll


def set_key(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = value
    elif type(dictionary[key]) == list:
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]


def getLocation(longitude,latitude):
    loc = {
        'type':'Point',
        'coordinates':[longitude, latitude]
    }
    return loc


def exchangerate_api_request(currency):
    '''
    Requests to exchangerate-api
    currency must be a string of three capital letters: e.g. EUR
    '''
    url = "https://api.exchangerate-api.com/v4/latest/{}".format(currency)
    res = requests.get(url)
    return res


def getCompaniesNear(longitude, latitude, max_distance_m=2000):
    db, coll = connectCollection('companies','companies_cleaned')
    return list(coll.find(
    {"office_1_location":{"$near":{"$geometry":{"type":"Point","coordinates":[longitude,latitude]},
                                   "$maxDistance":max_distance_m}}}))



