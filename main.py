
# Importing packages:
import pandas as pd
import numpy as np
import folium
import random
import fontawesome as fa
from src.api import *
from src.mongodb import *

########################################################################################################

df = pd.read_csv('./input/companies_df.csv', low_memory = False)
cols = ['_id', 'name', 'founded_year', 'category_code','deadpooled_year', 'total_money_raised_USD', 'num_offices',
 'office_1_longitude','office_1_latitude', 'office_1_location', 'office_1_city','office_1_state_code',
 'office_1_country_code']
df = df[cols]

########################################################################################################

# Importing db and col:

db, coll = connectCollection('companies','companies_cleaned')

companies = list(coll.find())

########################################################################################################

# Developers like to be near successful tech startups that have raised at least 1 Million dollars

# {$and:[{$or:[{category_code:'hardware'},{category_code:'nanotech'},{category_code:'mobile'},
# {category_code:'games_video'},{category_code:'cleantech'},{category_code:'software'},
# {category_code:'analytics'},{category_code:'web'},{category_code:'biotech'}]},{deadpooled_year: NaN},
# {founded_year:{$gte:2010}},{total_money_raised_USD:{$gte:1000000}}]}

successful_tech_startups = list(coll.find({'$and':[{'$or':[
        {'category_code':'semiconductor'},{'category_code':'network_hosting'},{'category_code':'consulting'},
        {'category_code':'design'},{'category_code':'hardware'},{'category_code':'nanotech'},
        {'category_code':'mobile'},{'category_code':'games_video'},{'category_code':'cleantech'},
        {'category_code':'software'},{'category_code':'analytics'},{'category_code':'web'},
        {'category_code':'biotech'}]},
    {'deadpooled_year': np.nan},{'founded_year':{'$gte':1999}},{'total_money_raised_USD':{'$gte':1000000}}]}))

possible_offices_criterion_1 = []
for e in successful_tech_startups:
    near_companies = getCompaniesNear(e['office_1_location']['coordinates'][0],
                                      e['office_1_location']['coordinates'][1],2000)
    # [near_companies[i] for i in range(len(near_companies)) if near_companies[i]['name'] == e['name']]
    # [near_companies[i] for i in range(len(near_companies)) if near_companies[i]['name'] != e['name']]
    for f in near_companies:
        if f['_id'] != e['name']:
            possible_offices_criterion_1.append(f['_id'])

possible_offices_c1 = list(set(possible_offices_criterion_1))

########################################################################################################

# Nobody in the company likes to have companies with more than 10 (13) years in a radius of 2 KM
# {$and:[{deadpooled_year: NaN},{founded_year:{$lte:2009}}]}

years= 13
old_companies = list(coll.find({'$and':[{'deadpooled_year': np.nan},{'founded_year':{'$lte':2019-years}}]}))

not_possible_offices_criterion_2 = []
for e in old_companies:
    near_companies = getCompaniesNear(e['office_1_location']['coordinates'][0],
                                      e['office_1_location']['coordinates'][1],2000)
    for f in near_companies:
        if f['_id'] != e['name']:
            not_possible_offices_criterion_2.append(f['_id'])

not_possible_offices_c2 = list(set(not_possible_offices_criterion_2))

########################################################################################################

# Taking into account both criteria:

possible_offices_c1_c2 = []
for e in possible_offices_c1:
    if e not in not_possible_offices_c2:
        possible_offices_c1_c2.append(e)        
possible_offices_c1_c2_to_string = [str(e) for e in possible_offices_c1_c2]

possible_offices_c1_c2_coords = []
for f in possible_offices_c1_c2:
    for e in companies:
        if e['_id'] == f:
            possible_offices_c1_c2_coords.append(e['office_1_location'])

########################################################################################################

# Executives like Starbucks A LOT. Ensure there's a starbucks not to far

starbucks_list = VenuesListbtquery(possible_offices_c1_c2_coords, possible_offices_c1_c2, 'starbucks', 1000)

cleaned_starbucks_list = []
for i in range(len(starbucks_list)):
    if len(starbucks_list[i][1]['response']['venues']) > 0:
        cleaned_starbucks_list.append([starbucks_list[i][0],
                                       starbucks_list[i][1]['response']['venues'][0]['location']['lat'],
                                       starbucks_list[i][1]['response']['venues'][0]['location']['lng'],
                                       starbucks_list[i][1]['response']['venues'][0]['location']['distance'],
                                       starbucks_list[i][1]['response']['venues'][0]['location']['formattedAddress']])
                
possible_offices_c1_c2_c3 = [e[0] for e in cleaned_starbucks_list]
possible_offices_c1_c2_c3_to_string = [str(e) for e in possible_offices_c1_c2_c3]

possible_offices_c1_c2_c3_coords = []
for f in possible_offices_c1_c2_c3:
    for e in companies:
        if e['_id'] == f:
            possible_offices_c1_c2_c3_coords.append(e['office_1_location'])

########################################################################################################

# The CEO is Vegan

# vegan_list = VenuesListbtquery(possible_offices_c1_c2_c3_coords, possible_offices_c1_c2_c3, 'vegan', 1000)
vegan_list = VenuesListbtcategory(possible_offices_c1_c2_c3_coords, possible_offices_c1_c2_c3,
             '4bf58dd8d48988d1d3941735', 1000)

cleaned_vegan_list = []
for i in range(len(vegan_list)):
    if len(vegan_list[i][1]['response']['venues']) > 0:
        cleaned_vegan_list.append([vegan_list[i][0],
                                   vegan_list[i][1]['response']['venues'][0]['location']['lat'],
                                   vegan_list[i][1]['response']['venues'][0]['location']['lng'],
                                   vegan_list[i][1]['response']['venues'][0]['location']['distance'],
                                   vegan_list[i][1]['response']['venues'][0]['location']['formattedAddress'],
                                   vegan_list[i][1]['response']['venues'][0]['name']])

possible_offices_c1_c2_c3_c4 = [e[0] for e in cleaned_vegan_list]
possible_offices_c1_c2_c3_c4_to_string = [str(e) for e in possible_offices_c1_c2_c3_c4]

possible_offices_c1_c2_c3_c4_coords = []
for f in possible_offices_c1_c2_c3_c4:
    for e in companies:
        if e['_id'] == f:
            possible_offices_c1_c2_c3_c4_coords.append(e['office_1_location'])

########################################################################################################

# All people in the company have between 25 and 40 years, give them some place to go to party

party_list = VenuesListbtcategory(possible_offices_c1_c2_c3_c4_coords, possible_offices_c1_c2_c3_c4,
 '4bf58dd8d48988d11f941735', 1000)

# party_list[0][1]['response']['venues'][0]

########################################################################################################

# Account managers need to travel a lot

########################################################################################################

# 30% of the company have at least 1 child

########################################################################################################

# Filtered DF:

indexs = []
for i in range(len(df)):
    if df['_id'][i] in possible_offices_c1_c2_c3_c4_to_string:
        indexs.append(i)

df_filtered = df.iloc[indexs]

########################################################################################################

# Folium map:

# Select one random row:
rowindex = random.choice(range(0,len(df_filtered)))
e = [df_filtered.iloc[rowindex][8], df_filtered.iloc[rowindex][7]]

lat_long_starbucks = []
distance_starbucks = 0
for i in range(len(cleaned_starbucks_list)):
    if str(cleaned_starbucks_list[i][0]) == df_filtered.iloc[rowindex][0]:
        lat_long_starbucks.append(cleaned_starbucks_list[i][1])
        lat_long_starbucks.append(cleaned_starbucks_list[i][2])
        distance_starbucks += cleaned_starbucks_list[i][3]

lat_long_vegan = []
distance_vegan = 0
name_vegan = ''
for i in range(len(cleaned_vegan_list)):
    if str(cleaned_vegan_list[i][0]) == df_filtered.iloc[rowindex][0]:
        lat_long_vegan.append(cleaned_vegan_list[i][1])
        lat_long_vegan.append(cleaned_vegan_list[i][2])
        distance_vegan += cleaned_vegan_list[i][3]
        name_vegan += cleaned_vegan_list[i][5]

# Output:
print(f"The perfect location for your business is in {df_filtered.iloc[rowindex][10]}, {df_filtered.iloc[rowindex][12]}.")
print(f"You don't have companies with more than {years} years in a radius of 2 KM (blue circle).")
print(f"The office is near successful tech startups that have raised at least 1 Million dollars.")
print(f"Your employees will find a Starbucks just {distance_starbucks} meters from the office.")
print(f"The vegan restaurant '{name_vegan}' can be found just {distance_vegan} meters from the office.")

# map_city
tooltip = 'Click me!'
map_city = folium.Map(location = e, zoom_start=13)
folium.Circle(radius=2000,location=e,popup='Old companies free zone',color='#3186cc',
    fill=True,fill_color='#3186cc').add_to(map_city)
folium.Marker(e,radius=2,icon=folium.Icon(
    icon='briefcase', color='red'),popup='<b>Perfect location for your business</b>',
    tooltip=tooltip).add_to(map_city)
folium.Marker(lat_long_starbucks,radius=2,icon=folium.Icon(
    icon='coffee', prefix='fa',color='orange'),popup='Starbucks',
    tooltip=tooltip).add_to(map_city)
folium.Marker(lat_long_vegan,radius=2,icon=folium.Icon(
    icon='cutlery',color='green'),popup=f"Vegan restaurant: '{name_vegan}'",
    tooltip=tooltip).add_to(map_city)
map_city
# map_city.save('./output/map.html')

