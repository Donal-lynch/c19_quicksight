# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 16:04:41 2020

@author: dolynch
"""


import requests
import json
import pandas as pd
import matplotlib.pyplot as plt


url = "https://covidapi.info/api/v1/country/"

payload  = {}
headers= {}

list_of_dfs = []

for country in ['IRL', 'ITA', 'ESP', 'GBR', 'USA']:
    response = requests.request("GET", url + country, headers=headers, data = payload)
    y = json.loads(response.text.encode('utf8'))
    df = pd.DataFrame.from_dict((y['result']), orient = 'index')
    df['country'] = country
        
    list_of_dfs.append(df)
    



def plot_with_norm_deaths(list_of_dfs, reference_deaths, set_axis_to_irl = False):
    
    # Make a new column for number of days since reference_deaths occured
    # This is to normalise the time axis on the plots


    for df in list_of_dfs:    
        # make a new column for the normalised day
        df['norm_day'] = df['deaths'].map(lambda x: True if (x >= reference_deaths) else False).cumsum()

    #df = pd.concat(list_of_dfs)



    for df in list_of_dfs:
    
        if len(df.loc[df['norm_day']>0, 'norm_day'] > 0):
            plt.plot(df.loc[df['norm_day']>0, 'norm_day']-1,
                     df.loc[df['norm_day']>0, 'deaths'],
                     label = df['country'][0])
       
            if not set_axis_to_irl:
                plt.text(x = df.loc[df['norm_day']>0, 'norm_day'].iloc[-1]-1,
                         y = df.loc[df['norm_day']>0, 'deaths'].iloc[-1]+250,
                         s = df['country'][0])
            
        if df['country'][0] == 'IRL':
            xlims = (0, df['norm_day'].max() + 2)
            ylims = (0, round(df['deaths'].max()*1.1))
    
    if set_axis_to_irl:
        plt.xlim(xlims)
        plt.ylim(ylims)
        plt.legend()
    else:    
        # set the x-axis lower limit to zero. Keep the upper limit the same
        plt.xlim(0, plt.gca().get_xlim()[1])
        

    plt.show()



plot_with_norm_deaths(list_of_dfs, reference_deaths = 1000, set_axis_to_irl = False)

plot_with_norm_deaths(list_of_dfs, reference_deaths = 10, set_axis_to_irl = True)



country_index = {}

for i in range(len(list_of_dfs)):
    country_index[list_of_dfs[i]['country'][0]] = i


list_of_dfs[country_index['GBR']]

for df in list_of_dfs:
    
    # df must be inorder
    df.sort_index(inplace = True)    
    # calculate the percent increase daily
    df['death_change'] = (df['deaths'] - df['deaths'].shift()) / df['deaths'].shift()        
    # make a new column for the normalised day
    df['norm_day'] = df['death_change'].map(lambda x: not pd.isnull(x)).cumsum() * 100




    if df['country'][0] != 'USA':
        plt.plot(df.loc[df['norm_day']>0, 'norm_day']-1,
                 df.loc[df['norm_day']>0, 'death_change'],
                 label = df['country'][0],
                 lw = 0.5,
                 alpha = 0.5)
        
        plt.scatter(df.loc[df['norm_day']>0, 'norm_day']-1,
                    df.loc[df['norm_day']>0, 'death_change'],
                    label = df['country'][0],
                    marker = 'o',
                    s = 3)
   
    
plt.legend()
plt.show()






