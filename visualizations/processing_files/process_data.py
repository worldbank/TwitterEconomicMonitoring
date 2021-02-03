import numpy as np
import pandas as pd
import os
from timeit import default_timer as timer
from os import listdir
from os.path import isfile, join
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from tqdm import tqdm
import math

# LOAD DATA
# 1. Users data
data_path = './Data/n_users_by_profile_location/'
files_parquet = [f for f in listdir(data_path) if isfile(join(data_path, f))]


print('Import Users By Account Locations')
start = timer()

l = []
for filename in files_parquet:
    if "SUCCESS" not in filename:
        try:
            df = pd.read_parquet(data_path + filename, engine='pyarrow')
            l.append(df)
        except:
            print('error importing', filename)
users_by_account_location = pd.concat(l, axis=0, ignore_index=True)
end = timer()
print('Computing Time:', round(end - start), 'sec')

# Location data
account_location = pd.read_excel("./Data/account_locations/account_locations_new.xlsx")
users_by_account_location = users_by_account_location.set_index("location").join\
							(account_location.set_index("user_location"), how="left")

data_by_country = users_by_account_location[(users_by_account_location["latitude"].notnull() &
                                         (users_by_account_location["longitude"].notnull()))][[
                                        'n_users','country_long',"country_short",'locality_long']].\
                                        groupby(['country_long']).sum().reset_index()

# Load data. We use data from World Bank's WDI
country_pop = pd.read_csv("./Data/Country/WDI_population.csv")
country_pop = country_pop.rename({"Country Name": "country_name", "Country Code": "country_code", "2020 [YR2020]":"population"}, 
                  axis = "columns" )[["country_name","country_code","population"]]
# And UN for some missing countries
missing_countries = pd.read_csv("./Data/Country/population_missing_countries.csv")

# I created this dictionary for merging
dict_pop = {}
rename_dict = {'Brunei Darussalam': "Brunei", 'Curacao':'Curaçao', "Cote d'Ivoire":"Côte d'Ivoire",
               'Czech Republic':'Czechia', 
         'Congo, Dem. Rep.': 'Democratic Republic of the Congo','Egypt, Arab Rep.':'Egypt',
         'Guyana':'French Guiana','Iran, Islamic Rep.':'Iran','Hong Kong SAR, China':'Hong Kong',
         'Kyrgyz Republic':'Kyrgyzstan','Lao PDR': "Laos",'Macao SAR, China':"Macau",'Myanmar': 'Myanmar (Burma)', 
        'Korea, Dem. People’s Rep.':'North Korea', 'Congo, Dem. Rep.': 'Democratic Republic of the Congo',
               'Congo, Rep.':'Republic of the Congo',
         'Russian Federation':"Russia",'St. Kitts and Nevis':'Saint Kitts and Nevis','St. Lucia':'Saint Lucia',
          'St. Vincent and the Grenadines': 'Saint Vincent and the Grenadines','Slovak Republic':'Slovakia',
          'Korea, Rep.':'South Korea','Bahamas, The':'The Bahamas','Gambia, The':"The Gambia",
          'Virgin Islands (U.S.)':'U.S. Virgin Islands','Venezuela, RB': 'Venezuela','Yemen, Rep.':"Yemen"}

for index, row in country_pop.iterrows(): 
    if row["country_name"] in rename_dict.keys():
        dict_pop[rename_dict[row["country_name"]]] = row["population"]
    else:
        dict_pop[row["country_name"]] = row["population"]
for index, row in missing_countries.iterrows():
    dict_pop[row["country_name"]] = row["population"]

# Merge data and transform to numeric
data_by_country["population"] = data_by_country['country_long'].apply(lambda x: (dict_pop[x]))
data_by_country["population"] = data_by_country["population"].apply(lambda x: x.replace(" ",""))
data_by_country["population"] = data_by_country["population"].apply(lambda x: int(x))
data_by_country["users_per_K"] = data_by_country["n_users"]/data_by_country["population"] * 1000

#Population
city_population = pd.read_excel('./Data/City/WUP2018-F12-Cities_Over_300K.xls', header = 16)
city_population = city_population[['Country Code','Country or area','City Code', 'Urban Agglomeration','Note',
                  'Latitude','Longitude',2020]]
top_100_cities = city_population.sort_values(2020, ascending=False)[:100]

dict_city_population = {}
for index, row in city_population.iterrows():
    l=[]
    l.append(row[2020]*1000)
    l.append(row["Country or area"])    
    dict_city_population[row['Urban Agglomeration']] = l 

# Users by city
data_by_city = users_by_account_location[(users_by_account_location["latitude"].notnull() &
                                         (users_by_account_location["longitude"].notnull()))][[
                                        'n_users','country_long',"country_short",'locality_long', 'latitude','longitude']].\
                                        groupby(['locality_long','country_long', 'latitude','longitude']).sum().reset_index()
data_by_city = data_by_city.sort_values("n_users", ascending=False)

def match_names(name, list_names, min_score=80):
    max_score = -1
    max_name = ''
    for x in list_names:
        score = fuzz.partial_ratio(name.lower(), x.lower())
        if (score > min_score) & (score > max_score):
            max_name = x
            max_score = score
    return max_name

dict_matches = {}
for city in tqdm(data_by_city["locality_long"]):
    match = match_names(city, city_population["Urban Agglomeration"].to_list())
    try:
        lat_pop = city_population[city_population['Urban Agglomeration']== match].iloc[0]['Latitude']
        long_pop = city_population[city_population['Urban Agglomeration']== match].iloc[0]['Longitude']
        lat_users = data_by_city[data_by_city["locality_long"]==city].iloc[0]['latitude']
        long_users = data_by_city[data_by_city["locality_long"]==city].iloc[0]['longitude']
        dif_lat = lat_pop - lat_users
        dif_long = long_pop - long_users
        if (abs(dif_lat)<1) & (abs(dif_long) < 1):
            dict_matches[city] = match
        else:
            dict_matches[city] = ''
    except:
        dict_matches[city] = ''
dict_matches['Lima']='Lima'
dict_matches["Bengaluru"]="Bangalore"
dict_matches['Seville'] = 'Sevilla'
dict_matches['Pekanbaru'] = 'Pekan Baru'
dict_matches['Islamabad']= 'Islamabad'
dict_matches['Richmond']= 'Richmond'
dict_matches['San Jose']= 'San Jose'
dict_matches['Buffalo']= 'Buffalo'
dict_matches['Batam']="Batam"
dict_matches['Santiago de Querétaro']= 'Querétaro'
dict_matches['Aguascalientes']='Aguascalientes'
dict_matches['Reno']='Reno'
dict_matches['Ribeirao Preto']="Savannah"
dict_matches['Mexicali']='Mexicali'
dict_matches['Irkutsk'] = 'Irkutsk'
dict_matches['Laredo'] = 'Laredo'

data_by_city["match_city"] = data_by_city['locality_long'].apply(lambda x: dict_matches[x])

data_by_city['population']=None
for index, row in data_by_city.iterrows():
    if row['match_city']=="":
        try:
            if row["country_long"] == dict_city_population[row['locality_long']][1]:
                data_by_city.at[index,'population'] = dict_city_population[row['locality_long']][0]
        except:
            pass
    else:
        try:
            if row["country_long"] == dict_city_population[row['locality_long']][1]:
                data_by_city.at[index,'population'] = dict_city_population[row['locality_long']][0]
        except:
            data_by_city.at[index,'population'] = dict_city_population[row['match_city']][0]
data_by_city["users_per_K"] = data_by_city["n_users"]/data_by_city["population"] * 1000
data_by_city.to_csv('./Data/twitter_coverage_cities.csv')

gdp = pd.read_csv("./Data/gdp_per_capita/gdp.csv")
gdp = gdp.rename({"Country Name": "country_name", "Country Code": "country_code", "2019 [YR2019]":"gdp_2019"}, 
                  axis = "columns" )[["country_name","country_code","gdp_2019"]]
dict_gdp = {}

for index, row in gdp.iterrows(): 
    if row["country_name"] in rename_dict.keys():
        dict_gdp[rename_dict[row["country_name"]]] = row["gdp_2019"]
    else:
        dict_gdp[row["country_name"]] = row["gdp_2019"]
dict_gdp["Venezuela"] = 2299 # Adding this missing val by hand

for index, row in data_by_country.iterrows():
    try:
        data_by_country.at[index,"gdp_2019"] = dict_gdp[row["country_long"]]
    except:
        data_by_country.at[index,"gdp_2019"] = np.nan
data_by_country = data_by_country[data_by_country["gdp_2019"]!=".."]
data_by_country["gdp_2019"] = data_by_country["gdp_2019"].apply(lambda x: float(x))       

data_by_country.to_csv('./Data/twitter_coverage_countries.csv')
