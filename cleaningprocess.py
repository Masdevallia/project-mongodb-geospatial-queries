
# Importing packages:
from src.CleanFilter import *
from src.mongodb import *
from src.api import exchangerate_api_request

def main():

    # Importing db and col:
    db, coll = connectCollection('companies','companies')
    companies = list(coll.find({'$or':[{"offices.latitude":{'$ne':None}},{"offices.longitude":{'$ne':None}}]}))

    ########################################################################################################

    # Dict to DF:
    companies_dict = {}
    for i in range(len(companies)):
        set_key(companies_dict, '_id', companies[i]['_id'])
        set_key(companies_dict, 'name', companies[i]['name'])
        set_key(companies_dict, 'founded_year', companies[i]['founded_year'])
        set_key(companies_dict, 'category_code', companies[i]['category_code'])
        set_key(companies_dict, 'total_money_raised', companies[i]['total_money_raised'])
        set_key(companies_dict, 'deadpooled_year', companies[i]['deadpooled_year'])

    companies_df = pd.DataFrame.from_dict(companies_dict)

    ########################################################################################################

    # Offices:
    num_offices = []
    for i in range(len(companies)):
        num_offices.append(len(companies[i]['offices']))
    companies_df['num_offices'] = num_offices

    for i in range(max(num_offices)):
        companies_df[f'office_{i+1}_longitude'] = [np.nan] * len(num_offices)
        companies_df[f'office_{i+1}_latitude'] = [np.nan] * len(num_offices)
        companies_df[f'office_{i+1}_location'] = [{}] * len(num_offices)
        companies_df[f'office_{i+1}_city'] = [None] * len(num_offices)
        companies_df[f'office_{i+1}_state_code'] = [None] * len(num_offices)
        companies_df[f'office_{i+1}_country_code'] = [None] * len(num_offices)

    companies_data = []
    for i in range(len(companies)):
        if len(companies[i]['offices'])==0:
            companies_data.append([[0, np.nan, np.nan, np.nan, np.nan, np.nan]])
        elif len(companies[i]['offices'])>0:
            aux_offices = []
            for j in range(len(companies[i]['offices'])):
                aux_offices.append([j+1, companies[i]['offices'][j]['latitude'], companies[i]['offices'][j]['longitude'],
                                    companies[i]['offices'][j]['city'], companies[i]['offices'][j]['state_code'],
                                    companies[i]['offices'][j]['country_code']])
            companies_data.append(aux_offices)

    for i in range(len(companies_data)):
        for j in range(len(companies_data[i])):
            if companies_data[i][j][0] != 0:
                companies_df.at[i, f'office_{j+1}_longitude'] = companies_data[i][j][2]
                companies_df.at[i, f'office_{j+1}_latitude'] = companies_data[i][j][1]
                companies_df.at[i, f'office_{j+1}_city'] = companies_data[i][j][3]
                companies_df.at[i, f'office_{j+1}_state_code'] = companies_data[i][j][4]
                companies_df.at[i, f'office_{j+1}_country_code'] = companies_data[i][j][5]


    ########################################################################################################

    # GeoJSON Objects:
    for i in range(len(companies_data)):
        for j in range(len(companies_data[i])):
            if companies_data[i][j][0] != 0:
                companies_df.at[i, f'office_{j+1}_location'] = getLocation(companies_df.at[i, f'office_{j+1}_longitude'],
                                                                        companies_df.at[i, f'office_{j+1}_latitude'])


    ########################################################################################################

    # Money raised:
    companies_df.total_money_raised.replace('$0','0', inplace=True)
    companies_df['total_money_raised_currency'] = [None] * len(num_offices)

    for i in range(len(companies_df)):
        if companies_df.at[i,'total_money_raised'] == '0':
            companies_df.at[i,'total_money_raised_currency'] = '$'
        else:
            companies_df.at[i,'total_money_raised_currency'] = companies_df.total_money_raised[i][0]
            companies_df.at[i,'total_money_raised'] = companies_df.total_money_raised[i][1:]

    for i in range(len(companies_df)):
        if companies_df.at[i,'total_money_raised'][0] == '$':
            companies_df.at[i,'total_money_raised_currency'] = companies_df.total_money_raised[i][0]
            companies_df.at[i,'total_money_raised'] = companies_df.total_money_raised[i][1:]

    companies_df.total_money_raised.replace('r21M','21M',inplace=True)

    for i in range(len(companies_df)):
        if companies_df.total_money_raised[i][-1] == 'M':
            companies_df.at[i,'total_money_raised'] = str(float(companies_df.total_money_raised[i].split('M')[0])*1000000)
        elif companies_df.total_money_raised[i][-1] == 'B':
            companies_df.at[i,'total_money_raised'] = str(float(companies_df.total_money_raised[i].split('B')[0])*1000000000)
        elif companies_df.total_money_raised[i][-1] == 'k':
            companies_df.at[i,'total_money_raised'] = str(float(companies_df.total_money_raised[i].split('k')[0])*1000)

    companies_df['total_money_raised'] = companies_df['total_money_raised'].astype('float')

    companies_df.total_money_raised_currency.replace('k','SEK',inplace=True)
    companies_df.total_money_raised_currency.replace('$','USD',inplace=True)
    companies_df.total_money_raised_currency.replace('£','GBP',inplace=True)
    companies_df.total_money_raised_currency.replace('¥','JPY',inplace=True)
    companies_df.total_money_raised_currency.replace('€','EUR',inplace=True)

    ########################################################################################################

    # deadpooled_year:
    companies_df.deadpooled_year.replace(1.0,2006,inplace=True) # 2005 + 1
    companies_df.deadpooled_year.replace(2.0,1998,inplace=True) # 1996 + 2
    companies_df.deadpooled_year.replace(3.0,2008,inplace=True) # 2005 + 3

    ########################################################################################################

    # Currency exchange from an API:
    companies_df_final = companies_df[companies_df.num_offices>0]

    exchangerateGBP = exchangerate_api_request('GBP').json()
    exchangerateSEK = exchangerate_api_request('SEK').json()
    exchangerateEUR = exchangerate_api_request('EUR').json()

    companies_df_final['total_money_raised_USD'] = [0.0]*len(companies_df_final)

    for i in range(len(companies_df_final)):
        if companies_df_final.at[i,'total_money_raised_currency'] == 'USD':
            companies_df_final.at[i,'total_money_raised_USD'] = companies_df_final.at[i,'total_money_raised']
        elif companies_df_final.at[i,'total_money_raised_currency'] == 'GBP':
            companies_df_final.at[i,'total_money_raised_USD'] = companies_df_final.at[i,'total_money_raised']*exchangerateGBP['rates']['USD']   
        elif companies_df_final.at[i,'total_money_raised_currency'] == 'SEK':
            companies_df_final.at[i,'total_money_raised_USD'] = companies_df_final.at[i,'total_money_raised']*exchangerateSEK['rates']['USD']   
        elif companies_df_final.at[i,'total_money_raised_currency'] == 'EUR':
            companies_df_final.at[i,'total_money_raised_USD'] = companies_df_final.at[i,'total_money_raised']*exchangerateEUR['rates']['USD']

    ########################################################################################################

    # Exporting cleaned csv:
    companies_df_final.to_csv('./input/companies_df.csv', index=False)
    companies_df_final.to_json('./input/cleaned_companies.json', orient="records")

    ########################################################################################################

    # Importing cleaned data to MongoDB and creating 2dSphere index:
    coll2 = db['companies_cleaned']
    coll2.insert_many(companies_df_final.to_dict('records'))

    # I think it could be done with this command, but I've done it from MongoDB Compass.
    # coll2.create_index([('office_1_location', pymongo.GEOSPHERE)])

if __name__=="__main__":
    main()