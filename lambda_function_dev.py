import json
from datetime import datetime
#import os
import requests
#import boto3

# Code adapted from: https://github.com/scochran3/data_acquisition_aws_lambda/blob/master/lambda_function.py
# Lambda and S3 tutorial is here: https://towardsdatascience.com/make-data-acquisition-easy-with-aws-lambda-python-in-12-steps-33fe201d1bb4
# API docs here: https://documenter.getpostman.com/view/2568274/SzS8rjbe?version=latest#e629a11a-695c-4dab-8eff-5e0594735507




#def lambda_handler(event, context):


def dict_to_csv(csv, res_dict, country):
    '''
    Convert a dictionary to csv like string
    Parameters
    ----------
    csv : string
        Formated as csv file
    res_dict : dictionary
        responce from API
    country : string
        the name of the country to which this data belongs

    Returns
    -------
    csv: string
        csv file with new data appended
    '''
    
    #csv += '\n'
    
    for key, value in res_dict.items():
        csv += key + ','
        
        csv += country + ','
        
        csv += ','.join(str(x) for x in value.values())
        
        csv += '\n'
        
     
    return csv   





for country in ['IRL', 'ITA', 'ESP', 'GBR', 'USA']:
    response = requests.request("GET", url + country, headers=headers, data = payload)

    y = json.loads(response.text.encode('utf8'))
    api_csv = dict_to_csv(csv = api_csv,
                          res_dict = y['result'],
                          country = country)

    
    







        

#','.join({'confirmed': 1, 'deaths': 0, 'recovered': 0}.values())
#', '.join(str(x) for x in {'confirmed': 1, 'deaths': 0, 'recovered': 0}.values())


temp = dict_to_csv(csv, res_dict = y['result'], country = 'IRL')








import pandas as pd
    
#df = pd.DataFrame.from_dict(json.loads(data)['IRL'])


    
    
df = pd.DataFrame.from_dict((y['result']), orient = 'index')
df['country'] = country
list_of_dfs.append(df)


df_as_dict = pd.concat(list_of_dfs).to_dict(orient = 'list')

# Convert data to json
data = json.dumps(temp)


#pd.DataFrame.from_dict(json.loads(data))   

# Get the current datetime for the file name
now = str(datetime.today())
	
# Export the data to S3
#client = boto3.client('s3')

#response = client.put_object(Bucket='c19datastore',
#                             Body=data, 
#                             Key='rawdata/{}.json'.format(now))


