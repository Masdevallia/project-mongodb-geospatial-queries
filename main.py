
# Importing packages:
import folium
import random
import fontawesome as fa
from src.CleanFilter import *
from src.api import *
from src.mongodb import *

# Importin data:
df = pd.read_csv('./input/companies_df.csv', low_memory = False)
cols = ['_id', 'name', 'founded_year', 'category_code','deadpooled_year', 'total_money_raised_USD', 'num_offices',
 'office_1_longitude','office_1_latitude', 'office_1_location', 'office_1_city','office_1_state_code',
 'office_1_country_code']
df = df[cols]

# Importing database and collection:
db, coll = connectCollection('companies','companies_cleaned')
companies = list(coll.find())

########################################################################################################

# Developers like to be near successful tech startups that have raised at least n (1 Million) dollars
# inputmoney = 1000000
inputmoney = 500000

successful_tech_startups = list(coll.find({'$and':[{'$or':[
        {'category_code':'semiconductor'},{'category_code':'network_hosting'},{'category_code':'consulting'},
        {'category_code':'design'},{'category_code':'hardware'},{'category_code':'nanotech'},
        {'category_code':'mobile'},{'category_code':'games_video'},{'category_code':'cleantech'},
        {'category_code':'software'},{'category_code':'analytics'},{'category_code':'web'},
        {'category_code':'biotech'}]},
    {'deadpooled_year': np.nan},{'founded_year':{'$gte':1999}},{'total_money_raised_USD':{'$gte':inputmoney}}]}))

startups_and_near_companies = []
possible_offices_criterion_1 = []
for e in successful_tech_startups:
    near_companies = getCompaniesNear(e['office_1_location']['coordinates'][0],
                                      e['office_1_location']['coordinates'][1],2000)
    aux = []
    aux.append([e['_id'], e['name'], e['founded_year'], e['category_code'], e['total_money_raised'], 
          e['office_1_longitude'], e['office_1_latitude']])
    aux.append([near_companies[i] for i in range(len(near_companies)) if near_companies[i]['name'] != e['name']])    
    startups_and_near_companies.append(aux)
    for f in near_companies:
        if f['_id'] != e['name']:
            possible_offices_criterion_1.append(f['_id'])
possible_offices_c1 = list(set(possible_offices_criterion_1))

########################################################################################################

# Nobody in the company likes to have companies with more than n (10) years in a radius of 2 KM
# inputyears= 10
inputyears= 15
old_companies = list(coll.find({'$and':[{'deadpooled_year': np.nan},{'founded_year':{'$lte':2019-inputyears}}]}))

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
possible_offices_c1_c2_coords = getOfficesCoords(possible_offices_c1_c2, companies)

########################################################################################################

# Executives like Starbucks A LOT. Ensure there's a starbucks not to far
starbucks_list = venuesListByQuery(possible_offices_c1_c2_coords, possible_offices_c1_c2, 'starbucks', 1000)
cleaned_starbucks_list = cleanVenueList(starbucks_list)              
possible_offices_c1_c2_c3 = [e[0] for e in cleaned_starbucks_list]
possible_offices_c1_c2_c3_to_string = [str(e) for e in possible_offices_c1_c2_c3]
possible_offices_c1_c2_c3_coords = getOfficesCoords(possible_offices_c1_c2_c3, companies)

########################################################################################################

# The CEO is Vegan
# vegan_list = venuesListByQuery(possible_offices_c1_c2_c3_coords, possible_offices_c1_c2_c3, 'vegan', 1000)
vegan_list = venuesListByCategory(possible_offices_c1_c2_c3_coords, possible_offices_c1_c2_c3,
             '4bf58dd8d48988d1d3941735', 1000)
cleaned_vegan_list = cleanVenueList(vegan_list)
possible_offices_c1_c2_c3_c4 = [e[0] for e in cleaned_vegan_list]
possible_offices_c1_c2_c3_c4_to_string = [str(e) for e in possible_offices_c1_c2_c3_c4]
possible_offices_c1_c2_c3_c4_coords = getOfficesCoords(possible_offices_c1_c2_c3_c4, companies)

########################################################################################################

# All people in the company have between 25 and 40 years, give them some place to go to party
party_list = venuesListByCategory(possible_offices_c1_c2_c3_c4_coords, possible_offices_c1_c2_c3_c4,
 '4bf58dd8d48988d11f941735', 1000)
cleaned_party_list = cleanVenueList(party_list)
possible_offices_c1_c2_c3_c4_c5 = [e[0] for e in cleaned_party_list]
possible_offices_c1_c2_c3_c4_c5_to_string = [str(e) for e in possible_offices_c1_c2_c3_c4_c5]
possible_offices_c1_c2_c3_c4_c5_coords = getOfficesCoords(possible_offices_c1_c2_c3_c4_c5, companies)

########################################################################################################

# Account managers need to travel a lot (Airport < 25 km)
airport_list = venuesListByCategory(possible_offices_c1_c2_c3_c4_c5_coords, possible_offices_c1_c2_c3_c4_c5,
 '4bf58dd8d48988d1ed931735', 25000)
cleaned_airport_list = cleanVenueList(airport_list)
possible_offices_c1_c2_c3_c4_c5_c6 = [e[0] for e in cleaned_airport_list]
possible_offices_c1_c2_c3_c4_c5_c6_to_string = [str(e) for e in possible_offices_c1_c2_c3_c4_c5_c6]
possible_offices_c1_c2_c3_c4_c5_c6_coords = getOfficesCoords(possible_offices_c1_c2_c3_c4_c5_c6, companies)

########################################################################################################

# 30% of the company have at least 1 child (Schools < 5 km)
school_list = venuesListByCategory(possible_offices_c1_c2_c3_c4_c5_c6_coords, 
possible_offices_c1_c2_c3_c4_c5_c6,
 ['4f4533804b9074f6e4fb0105', '4bf58dd8d48988d13d941735','52e81612bcbc57f1066b7a46',
 '52e81612bcbc57f1066b7a45','4f4533814b9074f6e4fb0107','4f4533814b9074f6e4fb0106'], 5000)
cleaned_school_list = cleanVenueList(school_list)
possible_offices_c1_c2_c3_c4_c5_c6_c7 = [e[0] for e in cleaned_school_list]
possible_offices_c1_c2_c3_c4_c5_c6_c7_to_string = [str(e) for e in possible_offices_c1_c2_c3_c4_c5_c6_c7]
possible_offices_c1_c2_c3_c4_c5_c6_c7_coords = getOfficesCoords(possible_offices_c1_c2_c3_c4_c5_c6_c7, companies)

########################################################################################################

# Filtered DF:
indexs = []
for i in range(len(df)):
    if df['_id'][i] in possible_offices_c1_c2_c3_c4_c5_c6_c7_to_string:
        indexs.append(i)
df_filtered = df.iloc[indexs]

########################################################################################################

# Folium map:

# Select one random row:
rowindex = random.choice(range(0,len(df_filtered)))

e = [df_filtered.iloc[rowindex][8], df_filtered.iloc[rowindex][7]]

lat_long_starbucks = getLatLongVenue(cleaned_starbucks_list, df_filtered, rowindex)
distance_starbucks = getDistanceVenue(cleaned_starbucks_list, df_filtered, rowindex)
lat_long_vegan = getLatLongVenue(cleaned_vegan_list, df_filtered, rowindex)
distance_vegan = getDistanceVenue(cleaned_vegan_list, df_filtered, rowindex)
name_vegan = getNameVenue(cleaned_vegan_list, df_filtered, rowindex)
lat_long_party = getLatLongVenue(cleaned_party_list, df_filtered, rowindex)
distance_party = getDistanceVenue(cleaned_party_list, df_filtered, rowindex)
name_party = getNameVenue(cleaned_party_list, df_filtered, rowindex)
lat_long_airport = getLatLongVenue(cleaned_airport_list, df_filtered, rowindex)
distance_airport = getDistanceVenue(cleaned_airport_list, df_filtered, rowindex)
name_airport = getNameVenue(cleaned_airport_list, df_filtered, rowindex)
lat_long_school = getLatLongVenue(cleaned_school_list, df_filtered, rowindex)
distance_school = getDistanceVenue(cleaned_school_list, df_filtered, rowindex)
name_school = getNameVenue(cleaned_school_list, df_filtered, rowindex)

# Output:
print(f"The perfect location for your business is in {df_filtered.iloc[rowindex][10]}, {df_filtered.iloc[rowindex][12]}.")
print(f"You don't have companies with more than {inputyears} years in a radius of 2 KM (blue circle).")
print(f"The office is near successful tech startups that have raised at least {inputmoney} dollars.")
print(f"Your employees will find a Starbucks just {distance_starbucks} meters from the office.")
print(f"The vegan restaurant '{name_vegan}' can be found just {distance_vegan} meters from the office.")
print(f"Party mood? You will find the night club called '{name_party}' just {distance_party} meters from the office.")
print(f"If you need to travel often, there is no problem. You have an airport ({name_airport}) just {distance_airport} meters from the office.")
print(f"And if that were not enough, your children could go to school ({name_school}) just {distance_school} meters from the office.")

# map_city
tooltip = 'Click me!'
map_city = folium.Map(location = e, zoom_start=14)
folium.Circle(radius=2000,location=e,popup='Old companies free zone',color='#3186cc',
    fill=True,fill_color='#3186cc').add_to(map_city)
folium.Marker(lat_long_starbucks,radius=2,icon=folium.Icon(
    icon='coffee', prefix='fa',color='orange'),popup='Starbucks',
    tooltip=tooltip).add_to(map_city)
folium.Marker(lat_long_vegan,radius=2,icon=folium.Icon(
    icon='cutlery',color='green'),popup=f"Vegan restaurant: '{name_vegan}'",
    tooltip=tooltip).add_to(map_city)
folium.Marker(lat_long_party,radius=2,icon=folium.Icon(
    icon='glass',color='purple'),popup=f"Night club: '{name_party}'",
    tooltip=tooltip).add_to(map_city)
folium.Marker(lat_long_airport,radius=2,icon=folium.Icon(
    icon='plane', prefix='fa',color='blue'),popup=f"Airport: '{name_airport}'",
    tooltip=tooltip).add_to(map_city)
folium.Marker(lat_long_school,radius=2,icon=folium.Icon(
    icon='graduation-cap', prefix='fa',color='gray'),popup=f"School: '{name_school}'",
    tooltip=tooltip).add_to(map_city)
folium.Marker(e,radius=2,icon=folium.Icon(
    icon='briefcase', color='red'),popup='<b>Perfect location for your business</b>',
    tooltip=tooltip).add_to(map_city)
map_city
# map_city.save('./output/map.html')

