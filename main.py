
print('\nPlease wait...')

# Importing packages:
from src.CleanFilter import *
from src.api import *
from src.mongodb import *
from src.input import *
from src.output import *

title()

# Importin data:
# df = pd.read_csv('./input/companies_df.csv', low_memory = False)
df = pd.read_json('./input/cleaned_companies.json')
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

input_money()
while True:
    inputmoney = input('n = ')
    try:
        inputmoney = int(inputmoney)
        break
    except ValueError:
        print('Please enter a valid integer')
        continue
print('\nPlease wait...')

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

input_year()

while True:
    inputyears = input('n = ')
    try:
        inputyears = int(inputyears)
        break
    except ValueError:
        print('Please enter a valid integer')
        continue

print('\nPlease wait...')

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
possible_offices_c1_c2 = valuesInCommon(possible_offices_c1, not_possible_offices_c2)
possible_offices_c1_c2_to_string = [str(e) for e in possible_offices_c1_c2]
possible_offices_c1_c2_coords = getOfficesCoords(possible_offices_c1_c2, companies)

########################################################################################################

# Account managers need to travel a lot (Airport < 20 km)
input_airport()
airports_df = pd.read_csv('./input/airports.csv', header=None,usecols=[1,2,3,4,6,7,12], 
                          names=['FacilityName', 'City', 'Country','3CharCode','Lat','Long','FacilityType'])
airports_df = airports_df[airports_df['FacilityType']=='airport']
airports_df.reset_index(drop=True, inplace=True)

distances = []
for e in possible_offices_c1_c2_coords:
    coords_1 = (e['coordinates'][1], e['coordinates'][0])
    dist = []
    for i in range(len(airports_df)):
        coords_2 = (airports_df.at[i,'Lat'],airports_df.at[i,'Long'])
        dist.append(geopy.distance.geodesic(coords_1, coords_2).km)
    distances.append(dist)    

office_airports = []
for i in range(len(distances)):
    aux = []
    aux.append(possible_offices_c1_c2[i])
    for j in range(len(distances[i])):
        if distances[i][j] <= 20:
            aux.append([airports_df.at[j,'FacilityName'],
                        distances[i][j],
                        airports_df.at[j,'Lat'],
                        airports_df.at[j,'Long']])
    office_airports.append(aux)

possible_offices_c1_c2_c3 = []
for e in office_airports:
    if len(e) >= 2:
        possible_offices_c1_c2_c3.append(e[0])

possible_offices_c1_c2_c3_to_string = [str(e) for e in possible_offices_c1_c2_c3]
possible_offices_c1_c2_c3_coords = getOfficesCoords(possible_offices_c1_c2_c3, companies)

########################################################################################################

# Executives like Starbucks A LOT. Ensure there's a starbucks not to far
input_starbucks()
starbucks_list = venuesListByQuery(possible_offices_c1_c2_c3_coords, possible_offices_c1_c2_c3,
                                  'starbucks', 1000)
cleaned_starbucks_list = cleanVenueList(starbucks_list)              
possible_offices_c1_c2_c3_c4 = [e[0] for e in cleaned_starbucks_list]
possible_offices_c1_c2_c3_c4_to_string = [str(e) for e in possible_offices_c1_c2_c3_c4]
possible_offices_c1_c2_c3_c4_coords = getOfficesCoords(possible_offices_c1_c2_c3_c4, companies)

########################################################################################################

# The CEO is Vegan
input_vegan()
# vegan_list = venuesListByQuery(possible_offices_c1_c2_c3_c4_coords, possible_offices_c1_c2_c3_c4, 'vegan', 1000)
vegan_list = venuesListByCategory(possible_offices_c1_c2_c3_c4_coords, possible_offices_c1_c2_c3_c4,
             '4bf58dd8d48988d1d3941735', 1000)
cleaned_vegan_list = cleanVenueList(vegan_list)
possible_offices_c1_c2_c3_c4_c5 = [e[0] for e in cleaned_vegan_list]
possible_offices_c1_c2_c3_c4_c5_to_string = [str(e) for e in possible_offices_c1_c2_c3_c4_c5]
possible_offices_c1_c2_c3_c4_c5_coords = getOfficesCoords(possible_offices_c1_c2_c3_c4_c5, companies)

########################################################################################################

# All people in the company have between 25 and 40 years, give them some place to go to party
input_party()
party_list = venuesListByCategory(possible_offices_c1_c2_c3_c4_c5_coords, possible_offices_c1_c2_c3_c4_c5,
 '4bf58dd8d48988d11f941735', 1000)
cleaned_party_list = cleanVenueList(party_list)
possible_offices_c1_c2_c3_c4_c5_c6 = [e[0] for e in cleaned_party_list]
possible_offices_c1_c2_c3_c4_c5_c6_to_string = [str(e) for e in possible_offices_c1_c2_c3_c4_c5_c6]
possible_offices_c1_c2_c3_c4_c5_c6_coords = getOfficesCoords(possible_offices_c1_c2_c3_c4_c5_c6, companies)

########################################################################################################

# 30% of the company have at least 1 child (Schools < 5 km)
input_school()
school_list = venuesListByCategory(possible_offices_c1_c2_c3_c4_c5_c6_coords, 
possible_offices_c1_c2_c3_c4_c5_c6,
 ['4f4533804b9074f6e4fb0105', '4bf58dd8d48988d13d941735','52e81612bcbc57f1066b7a46',
 '52e81612bcbc57f1066b7a45','4f4533814b9074f6e4fb0107','4f4533814b9074f6e4fb0106'], 5000)
cleaned_school_list = cleanVenueList(school_list)
possible_offices_c1_c2_c3_c4_c5_c6_c7 = [e[0] for e in cleaned_school_list]
possible_offices_c1_c2_c3_c4_c5_c6_c7_to_string = [str(e) for e in possible_offices_c1_c2_c3_c4_c5_c6_c7]
possible_offices_c1_c2_c3_c4_c5_c6_c7_coords = getOfficesCoords(possible_offices_c1_c2_c3_c4_c5_c6_c7, companies)

########################################################################################################

if len(possible_offices_c1_c2_c3_c4_c5_c6_c7_coords) < 1:
    print('''
        
        We are sorry, there aren't any available locations for your company in our database.
        ''')

else:
    print('''
    
        Please wait, in a few seconds we will offer you the perfect location for your company!
    ''')

    # Filtered DF:
    indexs = []
    for i in range(len(df)):
        if df['_id'][i] in possible_offices_c1_c2_c3_c4_c5_c6_c7_to_string:
            indexs.append(i)
    df_filtered = df.iloc[indexs]
    df_filtered.reset_index(drop=True, inplace=True)

    df_filtered = df_filtered[['_id', 'name', 'office_1_longitude', 'office_1_latitude', 'office_1_city','office_1_country_code']]
    
    df_filtered['starbucks_lat'] = getLatVenue(cleaned_starbucks_list, df_filtered)
    df_filtered['starbucks_long'] = getLongVenue(cleaned_starbucks_list, df_filtered)
    df_filtered['starbucks_dist'] = getDistanceVenue(cleaned_starbucks_list, df_filtered)
    df_filtered['vegan_name'] = getNameVenue(cleaned_vegan_list, df_filtered)
    df_filtered['vegan_lat'] = getLatVenue(cleaned_vegan_list, df_filtered)
    df_filtered['vegan_long'] = getLongVenue(cleaned_vegan_list, df_filtered)
    df_filtered['vegan_dist'] = getDistanceVenue(cleaned_vegan_list, df_filtered)
    df_filtered['party_name'] = getNameVenue(cleaned_party_list, df_filtered)
    df_filtered['party_lat'] = getLatVenue(cleaned_party_list, df_filtered)
    df_filtered['party_long'] = getLongVenue(cleaned_party_list, df_filtered)
    df_filtered['party_dist'] = getDistanceVenue(cleaned_party_list, df_filtered)
    df_filtered['school_name'] = getNameVenue(cleaned_school_list, df_filtered)
    df_filtered['school_lat'] = getLatVenue(cleaned_school_list, df_filtered)
    df_filtered['school_long'] = getLongVenue(cleaned_school_list, df_filtered)
    df_filtered['school_dist'] = getDistanceVenue(cleaned_school_list, df_filtered)

    print('What do you want to have closer? A Starbucks (write 1), a Vegan Restaurant (2), a Place to Party (3) or a School (4)?')
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
     
    if order == 1:
        sortby = 'starbucks_dist'
    elif order == 2:
        sortby = 'vegan_dist'
    elif order == 3:
        sortby = 'party_dist'
    elif order == 4:
        sortby = 'school_dist'

    df_filtered = df_filtered.sort_values([sortby], ascending=[True])

    e = [df_filtered.iloc[0][3], df_filtered.iloc[0][2]]

    lat_long_starbucks = [df_filtered.iloc[0][6], df_filtered.iloc[0][7]]
    distance_starbucks = df_filtered.iloc[0][8]
    lat_long_vegan = [df_filtered.iloc[0][10], df_filtered.iloc[0][11]]
    distance_vegan = df_filtered.iloc[0][12]
    name_vegan = df_filtered.iloc[0][9]
    lat_long_party = [df_filtered.iloc[0][14], df_filtered.iloc[0][15]]
    distance_party = df_filtered.iloc[0][16]
    name_party = df_filtered.iloc[0][13]
    lat_long_school = [df_filtered.iloc[0][18], df_filtered.iloc[0][19]]
    distance_school = df_filtered.iloc[0][20]
    name_school = df_filtered.iloc[0][17]

    name_dist_lat_long_airport = []
    for i in range(len(office_airports)):
        if str(office_airports[i][0]) == df_filtered.iloc[0][0]:
            for j in range(1, len(office_airports[i])):
                name_dist_lat_long_airport.append(office_airports[i][j][0]) # name
                name_dist_lat_long_airport.append(office_airports[i][j][1]) # dist           
                name_dist_lat_long_airport.append(office_airports[i][j][2]) # lat
                name_dist_lat_long_airport.append(office_airports[i][j][3]) # long  

    near_startups = []
    for i in range(len(startups_and_near_companies)):
        for company in startups_and_near_companies[i][1]:
            if company['name'] == df_filtered.iloc[0][1]:
                near_startups.append(startups_and_near_companies[i][0])

    # Output:
    printoutput(df_filtered.iloc[0][4], df_filtered.iloc[0][5], inputyears,
    inputmoney, distance_starbucks, name_vegan, distance_vegan, name_party, distance_party,
    int(len(name_dist_lat_long_airport)/4), name_school, distance_school)

    # Folium map:
    tooltip = 'Click me!'
    map_city = folium.Map(location = e, zoom_start=11)
    folium.Circle(radius=2000,location=e,popup='Old companies free zone',color='#3186cc',
        fill=True,fill_color='#3186cc').add_to(map_city)
    folium.Marker(lat_long_starbucks,radius=2,icon=folium.Icon(
        icon='coffee', prefix='fa',color='orange'),popup='<b>[Starbucks]</b>',
        tooltip=tooltip).add_to(map_city)
    folium.Marker(lat_long_vegan,radius=2,icon=folium.Icon(
        icon='cutlery',color='green'),popup=f"<b>[Vegan restaurant]</b> '{name_vegan}'",
        tooltip=tooltip).add_to(map_city)
    folium.Marker(lat_long_party,radius=2,icon=folium.Icon(
        icon='glass',color='purple'),popup=f"<b>[Night club]</b> '{name_party}'",
        tooltip=tooltip).add_to(map_city)
    for i in range(0,len(name_dist_lat_long_airport),4):
        folium.Marker([name_dist_lat_long_airport[i+2],name_dist_lat_long_airport[i+3]],radius=2,icon=folium.Icon(
            icon='plane', prefix='fa',color='blue'),
            popup=f"<b>[Airport]</b> '{name_dist_lat_long_airport[i+0]}'. Distance from the office: {int(name_dist_lat_long_airport[i+1])} km",
            tooltip=tooltip).add_to(map_city)
    folium.Marker(lat_long_school,radius=2,icon=folium.Icon(
        icon='graduation-cap', prefix='fa',color='gray'),popup=f"<b>[School]</b> '{name_school}'",
        tooltip=tooltip).add_to(map_city)
    folium.Marker(e,radius=2,icon=folium.Icon(
        icon='briefcase', color='red'),popup='<b>Perfect location for your business</b>',
        tooltip=tooltip).add_to(map_city)
    for startup in near_startups:
        category = re.sub("_"," ",startup[3].capitalize())
        folium.Marker([startup[6], startup[5]],radius=2,icon=folium.Icon(
            icon='building-o', prefix='fa',color='black'),
            popup=f"<b>[Startup]</b> {startup[1]}. Founded year: {int(startup[2])}. Category: {category}. Total money raised (USD): {int(startup[4])}.",
            tooltip=tooltip).add_to(map_city) 
    map_city.save('./output/map.html')
    url = "file://{}{}{}".format(str(Path(os.getcwd())),"/output", "/map.html")
    webbrowser.open(url, 2)
