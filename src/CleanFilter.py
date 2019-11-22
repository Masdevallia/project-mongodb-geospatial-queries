
import pandas as pd
import numpy as np
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


def getIntegerInput():
    while True:
        getinput = input('n = ')
        try:
            getinput = int(getinput)
            break
        except ValueError:
            print('Please enter a valid integer')
            continue
    return getinput


def getDelimitedIntegerInput():
    while True:
        order = input('Your priority = ')
        try:
            order = int(order)
            if order > 0 and order < 5:
                break
            else:
                print('Please enter a valid integer: 1 for Starbucks; 2 for Vegan Restaurant; 3 for Place to Party; 4 for School.') 
        except ValueError:
            print('Please enter a valid integer: 1 for Starbucks; 2 for Vegan Restaurant; 3 for Place to Party; 4 for School.')
            continue
    return order


def calculateDistance(fromThis, toThis):
    distances = []
    for e in fromThis:
        coords_1 = (e['coordinates'][1], e['coordinates'][0])
        dist = []
        for i in range(len(toThis)):
            coords_2 = (toThis.at[i,'Lat'],toThis.at[i,'Long'])
            dist.append(geopy.distance.geodesic(coords_1, coords_2).km)
        distances.append(dist)   
    return distances 


def getCloserAirports(distances, offices, airports):
    office_airports = []
    for i in range(len(distances)):
        aux = []
        aux.append(offices[i])
        for j in range(len(distances[i])):
            if distances[i][j] <= 20:
                aux.append([airports.at[j,'FacilityName'],
                            distances[i][j],
                            airports.at[j,'Lat'],
                            airports.at[j,'Long']])
        office_airports.append(aux)
    return office_airports