
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()


def foursquare_request_venues_authorized(request, latitude, longitude, myquery, limit=1, radius = 1000):
    '''
    Requests to foursquare-api:
    Input:
    request: string:
    1) 'search': Returns a list of venues near the current location, matching a search term.
    2) 'explore': Returns a list of recommended venues near the current location.
    ll = '40.7243,-74.0018'.
    query = a search term to be applied against venue names: 'coffee'.
    limit = number of results to return, up to 50. Defaults to 1.
    radius = Limit results to venues within this many meters of the specified location. Defaults to 1km.
    '''
    url = 'https://api.foursquare.com/v2/venues/{}'.format(request)
    params = dict(
        client_id = os.getenv("FOURSQUARE_CLIENT_ID"),
        client_secret = os.getenv("FOURSQUARE_CLIENT_SECRET"),
        v='20180323', # version parameter
        ll='{},{}'.format(latitude,longitude),  
        query= myquery,
        limit=limit,
        radius=radius
    )
    resp = requests.get(url=url, params=params)
    return json.loads(resp.text)


def exchangerate_api_request(currency):
    '''
    Requests to exchangerate-api
    currency must be a string of three capital letters: e.g. EUR
    '''
    url = "https://api.exchangerate-api.com/v4/latest/{}".format(currency)
    res = requests.get(url)
    return res