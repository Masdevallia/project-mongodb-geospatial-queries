
# Importing packages:
from src.CleanFilter import *
from src.api import *
from src.mongodb import *
from src.input import *
from src.output import *

def main():

    title()

    # Importing data:
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
    input_money()
    inputmoney = getIntegerInput()
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
        aux.append([near_companies[i]['name'] for i in range(len(near_companies)) if near_companies[i]['name'] != e['name']])    
        startups_and_near_companies.append(aux)
        for f in near_companies:
            if f['_id'] != e['name']:
                possible_offices_criterion_1.append(f['_id'])
    possible_offices_c1 = list(set(possible_offices_criterion_1))

    ########################################################################################################

    # Nobody in the company likes to have companies with more than n (10) years in a radius of 2 KM
    input_year()
    inputyears = getIntegerInput()
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
    possible_offices_c1_c2_coords = getOfficesCoords(possible_offices_c1_c2, companies)

    ########################################################################################################

    # Account managers need to travel a lot (Airport < 20 km)
    input_airport()
    airports_df = pd.read_csv('./input/airports.csv', header=None,usecols=[1,2,3,4,6,7,12], 
                            names=['FacilityName', 'City', 'Country','3CharCode','Lat','Long','FacilityType'])
    airports_df = airports_df[airports_df['FacilityType']=='airport']
    airports_df.reset_index(drop=True, inplace=True)

    distances = calculateDistance(possible_offices_c1_c2_coords, airports_df)
    office_airports = getCloserAirports(distances, possible_offices_c1_c2, airports_df)
    possible_offices_c1_c2_c3 = []
    for e in office_airports:
        if len(e) >= 2:
            possible_offices_c1_c2_c3.append(e[0])
    possible_offices_c1_c2_c3_coords = getOfficesCoords(possible_offices_c1_c2_c3, companies)

    ########################################################################################################

    # Executives like Starbucks A LOT. Ensure there's a starbucks not to far
    input_starbucks()
    starbucks_list = venuesListByQuery(possible_offices_c1_c2_c3_coords, possible_offices_c1_c2_c3,
                                    'starbucks', 1000)
    cleaned_starbucks_list = cleanVenueList(starbucks_list)              
    possible_offices_c1_c2_c3_c4 = [e[0] for e in cleaned_starbucks_list]
    possible_offices_c1_c2_c3_c4_coords = getOfficesCoords(possible_offices_c1_c2_c3_c4, companies)

    ########################################################################################################

    # The CEO is Vegan
    input_vegan()
    vegan_list = venuesListByCategory(possible_offices_c1_c2_c3_c4_coords, possible_offices_c1_c2_c3_c4,
                '4bf58dd8d48988d1d3941735', 1000)
    cleaned_vegan_list = cleanVenueList(vegan_list)
    possible_offices_c1_c2_c3_c4_c5 = [e[0] for e in cleaned_vegan_list]
    possible_offices_c1_c2_c3_c4_c5_coords = getOfficesCoords(possible_offices_c1_c2_c3_c4_c5, companies)

    ########################################################################################################

    # All people in the company have between 25 and 40 years, give them some place to go to party
    input_party()
    party_list = venuesListByCategory(possible_offices_c1_c2_c3_c4_c5_coords, possible_offices_c1_c2_c3_c4_c5,
    '4bf58dd8d48988d11f941735', 1000)
    cleaned_party_list = cleanVenueList(party_list)
    possible_offices_c1_c2_c3_c4_c5_c6 = [e[0] for e in cleaned_party_list]
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
        
        formatList = ['vegan', 'party', 'school']
        i = 0
        for e in [cleaned_vegan_list, cleaned_party_list, cleaned_school_list]:
            df_filtered[f'{formatList[i]}_name'] = getNameVenue(e, df_filtered)
            df_filtered[f'{formatList[i]}_lat'] = getLatVenue(e, df_filtered)
            df_filtered[f'{formatList[i]}_long'] = getLongVenue(e, df_filtered)
            df_filtered[f'{formatList[i]}_dist'] = getDistanceVenue(e, df_filtered)
            i += 1

        print('''
            What do you prefer to have closer?
            A Starbucks (write 1), a Vegan Restaurant (2), a Place to Party (3) or a School (4)?''')  
        order = getDelimitedIntegerInput()           
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

        name_dist_lat_long_airport = []
        for i in range(len(office_airports)):
            if str(office_airports[i][0]) == df_filtered.iloc[0][0]:
                for j in range(1, len(office_airports[i])):
                    name_dist_lat_long_airport.append(office_airports[i][j][0])
                    name_dist_lat_long_airport.append(office_airports[i][j][1])           
                    name_dist_lat_long_airport.append(office_airports[i][j][2])
                    name_dist_lat_long_airport.append(office_airports[i][j][3])  

        near_startups = []
        for i in range(len(startups_and_near_companies)):
            if df_filtered.iloc[0][1] in startups_and_near_companies[i][1]:
                near_startups.append(startups_and_near_companies[i][0]) 

        ###################################################################################################

        # Output:
        printoutput(df_filtered.iloc[0][4], df_filtered.iloc[0][5], inputyears,
        inputmoney, df_filtered.iloc[0][8], df_filtered.iloc[0][9], df_filtered.iloc[0][12], df_filtered.iloc[0][13], df_filtered.iloc[0][16],
        int(len(name_dist_lat_long_airport)/4), df_filtered.iloc[0][17], df_filtered.iloc[0][20])

        # Folium map:
        foliumMap(e, [df_filtered.iloc[0][6], df_filtered.iloc[0][7]], 
                [df_filtered.iloc[0][10], df_filtered.iloc[0][11]], df_filtered.iloc[0][9],
                [df_filtered.iloc[0][14], df_filtered.iloc[0][15]], df_filtered.iloc[0][13],
                name_dist_lat_long_airport,
                [df_filtered.iloc[0][18], df_filtered.iloc[0][19]], df_filtered.iloc[0][17],
                near_startups)

if __name__=="__main__":
    main()