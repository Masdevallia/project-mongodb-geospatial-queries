
# Importing packages:
from src.mongodb import *
from src.clean import *
from src.api import foursquare_request_venues_authorized
import folium
import random

########################################################################################################

df = pd.read_csv('./input/companies_df.csv')

cols = ['_id', 'name', 'founded_year', 'category_code','deadpooled_year', 'total_money_raised_USD', 'num_offices',
 'office_1_longitude','office_1_latitude', 'office_1_location', 'office_1_city','office_1_state_code',
 'office_1_country_code']
df = df[cols]

########################################################################################################

# Importing db and col:

db, coll = connectCollection('companies','companies_cleaned')

companies = list(coll.find())

# active_companies = list(coll.find({'deadpooled_year': np.nan}))

########################################################################################################

# Nobody in the company likes to have companies with more than 10 years in a radius of 2 KM.

# {$and:[{deadpooled_year: NaN},{founded_year:{$lte:2009}}]}

# 13 years!
years= 13
old_companies = list(coll.find({'$and':[{'deadpooled_year': np.nan},{'founded_year':{'$lte':2019-years}}]}))

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

# Developers like to be near successful tech startups that have raised at least 1 Million dollars.

# {$and:[{$or:[{category_code:'hardware'},{category_code:'nanotech'},{category_code:'mobile'},
# {category_code:'games_video'},{category_code:'cleantech'},{category_code:'software'},
# {category_code:'analytics'},{category_code:'web'},{category_code:'biotech'}]},{deadpooled_year: NaN},
# {founded_year:{$gte:2010}},{total_money_raised_USD:{$gte:1000000}}]}

successful_tech_startups = list(coll.find({'$and':[{'$or':[
        {'category_code':'semiconductor'},{'category_code':'network_hosting'},{'category_code':'ecommerce'},
        {'category_code':'photo_video'},{'category_code':'consulting'},{'category_code':'design'},
        {'category_code':'automotive'},{'category_code':'hardware'},{'category_code':'nanotech'},
        {'category_code':'mobile'},{'category_code':'security'},{'category_code':'games_video'},
        {'category_code':'cleantech'},{'category_code':'software'},{'category_code':'analytics'},
        {'category_code':'web'},{'category_code':'biotech'}]},
    {'deadpooled_year': np.nan},{'founded_year':{'$gte':1976}},{'total_money_raised_USD':{'$gte':1000000}}]}))

not_possible_offices_criterion_2 = []
for e in old_companies:
    near_companies = getCompaniesNear(e['office_1_location']['coordinates'][0],
                                      e['office_1_location']['coordinates'][1],2000)
    for f in near_companies:
        if f['_id'] != e['name']:
            not_possible_offices_criterion_2.append(f['_id'])

not_possible_offices_c2 = list(set(not_possible_offices_criterion_2))

########################################################################################################

# Designers like to go to design talks and share knowledge. There must be some nearby companies 
# that also do design.

# design_companies = list(coll.find({'category_code':'design'}))

########################################################################################################

possible_offices_c1_c2 = []
for e in possible_offices_c1:
    if e not in not_possible_offices_c2:
        possible_offices_c1_c2.append(e)        
possible_offices_c1_c2_to_string = [str(e) for e in possible_offices_c1_c2]

########################################################################################################

indexs = []
for i in range(len(df)):
    if df['_id'][i] in possible_offices_c1_c2_to_string:
        indexs.append(i)
print(len(indexs))
print(indexs)

df_filtered = df.iloc[indexs]

########################################################################################################

possible_offices_c1_c2_coords = []
for e in companies:
    for f in possible_offices_c1_c2:
        if e['_id'] == f:
            possible_offices_c1_c2_coords.append(e['office_1_location'])

########################################################################################################

data = foursquare_request_venues_authorized('explore', selected_restaurant.values[0][4], selected_restaurant.values[0][5], 'cinema')

########################################################################################################

# map_city

tooltip = 'Click me!'
e = possible_offices_c1_c2_coords[random.choice(range(0,len(possible_offices_c1_c2_coords)))]
map_city = folium.Map(location = e['coordinates'][::-1], zoom_start=13)
folium.Circle(radius=2000,location=e['coordinates'][::-1],popup='Old companies free zone',color='#3186cc',
    fill=True,fill_color='#3186cc').add_to(map_city)
folium.Marker(e['coordinates'][::-1],radius=2,icon=folium.Icon(
    icon='briefcase',color='red'),popup='<b>Perfect location for your business</b>',
    tooltip=tooltip).add_to(map_city)
map_city

# map_city.save('./output/index.html')

