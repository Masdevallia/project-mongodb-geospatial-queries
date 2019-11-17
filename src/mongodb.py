
import pandas as pd
import numpy as np
from pymongo import MongoClient


def connectCollection(database, collection):
    '''
    Establishes the connection to a database and collection
    '''
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll


def getLocation(longitude,latitude):
    '''
    Returns a GeoJSON object
    '''
    loc = {
        'type':'Point',
        'coordinates':[longitude, latitude]
    }
    return loc


def getCompaniesNear(longitude, latitude, max_distance_m=2000):
    '''
    Returns all companies close to a certain longitude and latitude.
    Maximum distance defaults to 2km.
    '''
    db, coll = connectCollection('companies','companies_cleaned')
    return list(coll.find(
    {"office_1_location":{"$near":{"$geometry":{"type":"Point","coordinates":[longitude,latitude]},
                                   "$maxDistance":max_distance_m}}}))
