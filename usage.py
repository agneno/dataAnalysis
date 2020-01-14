import requests
import pandas as pd
import pandas_profiling
import os
import json

DATA_READ_STEP = 1000

mylist = []
# Loop through each page
resultRecordCount = requests.get('https://zemelapiai.vplanas.lt/arcgis/rest/services/Open_Data/Nekilnojamas_turtas/MapServer/0/query?where=1%3D1&outFields=*&returnCountOnly=true&f=json')
observationsCount = resultRecordCount.json()['count']

for resultOffset in list(range(0, observationsCount, DATA_READ_STEP)):

    # Construct the query
    base_endpoint = 'https://zemelapiai.vplanas.lt/arcgis/rest/services/Open_Data/Nekilnojamas_turtas/MapServer/0/query?where=1%3D1&outFields=*&f=json'

    # Configuration
    params = {
    'resultOffset': resultOffset,  # Need to read all data from API
    }
    # request the url and store the response in a variable
    response = requests.get(base_endpoint,params=params)

    # loop through each item
    usage = response.json()['features']
    for attributes in usage:
        mydict = {}  # initialize an empty dictionary to store data for each object
        mydict['Plotas_m2'] = attributes['attributes']['Plotas_m2']
        mydict['Charakter'] = attributes['attributes']['Charakter']
        mydict['Naud_Pask'] = attributes['attributes']['Naud_Pask']
        mylist.append(mydict)  # append the dictionary to mylist
        # convert the list to a pandas dataframe
        df = pd.DataFrame(mylist)

# Making overview of usage: grouping data by 'Naud_Pask' and 'Character'. 
# Calculating sum of 'Plotas_m2' and saving data to excel file.
usagegroupingby = df.groupby(['Naud_Pask', 'Charakter']).sum()
os.makedirs('results', exist_ok=True)
outputFileXlsx = 'results/usagegroupingby.xlsx'
usagegroupingby.to_excel(outputFileXlsx)
print(f'Created output file: {outputFileXlsx}')

# EDA using pandas profiling
profile = pandas_profiling.ProfileReport(
    df,
    title='Usage overview report',
    # removing correlation from report
    correlations={
        'recoded': {'calculate': False},
        'kendall': {'calculate': False},
        'phi_k': {'calculate': False},
        'cramers': {'calculate': False},
        'spearman': {'calculate': False},
        'pearson': {'calculate': False},
    },
)
outputFileHtml = 'results/usage.html'
profile.to_file(outputFileHtml)
print(f'Created output file: {outputFileHtml}')
        