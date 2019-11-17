
import pandas as pd
import numpy as np

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