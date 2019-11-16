
# Importing packages:

from pymongo import MongoClient
import pandas as pd
import numpy as np
import folium
from src.functions import connectCollection

########################################################################################################

# Importing db and col:

db, coll = connectCollection('companies','companies_cleaned')

companies = list(coll.find())

active_companies = list(coll.find({'deadpooled_year': np.nan}))

########################################################################################################

# Nobody in the company likes to have companies with more than 10 years in a radius of 2 KM.

# {$and:[{deadpooled_year: NaN},{founded_year:{$lte:2009}}]}

old_companies = list(coll.find({'$and':[{'deadpooled_year': np.nan},{'founded_year':{'$lte':2009}}]}))

########################################################################################################

# Developers like to be near successful tech startups that have raised at least 1 Million dollars.

# {$and:[{$or:[{category_code:'hardware'},{category_code:'nanotech'},{category_code:'mobile'},{category_code:'games_video'},{category_code:'cleantech'},{category_code:'software'},{category_code:'analytics'},{category_code:'web'},{category_code:'biotech'}]},{deadpooled_year: NaN},{founded_year:{$gte:2010}},{total_money_raised_USD:{$gte:1000000}}]}

successful_tech_startups_2010 = list(coll.find(
    {'$and':[{'$or':[{'category_code':'hardware'},{'category_code':'nanotech'},{'category_code':'mobile'},
                     {'category_code':'games_video'},{'category_code':'cleantech'},{'category_code':'software'},
                     {'category_code':'analytics'},{'category_code':'web'},{'category_code':'biotech'}]},
             {'deadpooled_year': np.nan},{'founded_year':{'$gte':2010}},{'total_money_raised_USD':{'$gte':1000000}}]}))

successful_tech_startups_2000 = list(coll.find(
    {'$and':[{'$or':[{'category_code':'hardware'},{'category_code':'nanotech'},{'category_code':'mobile'},
                     {'category_code':'games_video'},{'category_code':'cleantech'},{'category_code':'software'},
                     {'category_code':'analytics'},{'category_code':'web'},{'category_code':'biotech'}]},
             {'deadpooled_year': np.nan},{'founded_year':{'$gte':2000}},{'total_money_raised_USD':{'$gte':1000000}}]}))

########################################################################################################

# Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.

design_companies = list(coll.find({'category_code':'design'}))

########################################################################################################

# Folium

manhattan_companies = coll.find(
    {"office_1_location":{"$near":{"$geometry":{"type":"Point","coordinates":[-73.9712,40.7831]},
                                   "$maxDistance":3000}}})
# "$maxDistance":10000,"$minDistance":5000

manhattan_companies = list(manhattan_companies)

map_city = folium.Map(location=[40.7221,-73.9712], zoom_start=12)
for company in manhattan_companies:
    folium.Marker(company['office_1_location']['coordinates'][::-1],
                    radius=2,
                    icon=folium.Icon(icon='cloud',color='red'), 
                   ).add_to(map_city)

map_city

