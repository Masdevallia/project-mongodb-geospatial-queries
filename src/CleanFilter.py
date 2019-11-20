
import pandas as pd
import numpy as np

import folium
import random
import re
import fontawesome as fa
from pathlib import Path
import webbrowser
import geopy.distance


def set_key(dictionary, key, value):
    '''
    Function that fills dictionaries.
    Create keys if they do not yet exist and/or add values to existing keys.
    '''
    if key not in dictionary:
        dictionary[key] = value
    elif type(dictionary[key]) == list:
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]


def valuesInCommon(List1, List2):
    aux = []
    for e in List1:
        if e not in List2:
            aux.append(e)
    return aux


def getOfficesCoords(officesID, collection):
    aux = []
    for f in officesID:
        for e in collection:
            if e['_id'] == f:
                aux.append(e['office_1_location'])
    return aux


def cleanVenueList(venueList):
    aux = []
    for i in range(len(venueList)):
        if len(venueList[i][1]['response']['venues']) > 0:
            aux.append([venueList[i][0],
                venueList[i][1]['response']['venues'][0]['location']['lat'],
                venueList[i][1]['response']['venues'][0]['location']['lng'],
                venueList[i][1]['response']['venues'][0]['location']['distance'],
                venueList[i][1]['response']['venues'][0]['location']['formattedAddress'],
                venueList[i][1]['response']['venues'][0]['name']])
    return aux


def getLatVenue(venueList, df):
    latitude = []
    for j in range(len(df)):
        for i in range(len(venueList)):
            if df.iloc[j][0] == str(venueList[i][0]):
                latitude.append(venueList[i][1])
    return latitude
    

def getLongVenue(venueList, df):
    longitude = []
    for j in range(len(df)):
        for i in range(len(venueList)):
            if df.iloc[j][0] == str(venueList[i][0]):
                longitude.append(venueList[i][2])   
    return longitude


def getDistanceVenue(venueList, df):
    distance = []
    for j in range(len(df)):
        for i in range(len(venueList)):
            if df.iloc[j][0] == str(venueList[i][0]):
                distance.append(venueList[i][3])     
    return distance


def getNameVenue(venueList, df):
    name = []
    for j in range(len(df)):
        for i in range(len(venueList)):
            if df.iloc[j][0] == str(venueList[i][0]):
                name.append(venueList[i][5])    
    return name


'''
def getLatLongVenue(venueList, df, rowindex):
    aux = []
    for i in range(len(venueList)):
        if str(venueList[i][0]) == df.iloc[rowindex][0]:
            aux.append(venueList[i][1])
            aux.append(venueList[i][2])
    return aux


def getDistanceVenue(venueList, df, rowindex):
    aux = 0
    for i in range(len(venueList)):
        if str(venueList[i][0]) == df.iloc[rowindex][0]:
            aux += venueList[i][3]
    return aux


def getNameVenue(venueList, df, rowindex):
    aux = ''
    for i in range(len(venueList)):
        if str(venueList[i][0]) == df.iloc[rowindex][0]:
            aux += venueList[i][5]
    return aux
'''