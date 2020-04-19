import json
from datetime import datetime
import requests
import boto3
from io import StringIO


# Code adapted from: https://github.com/scochran3/data_acquisition_aws_lambda/blob/master/lambda_function.py
# Lambda and S3 tutorial is here: https://towardsdatascience.com/make-data-acquisition-easy-with-aws-lambda-python-in-12-steps-33fe201d1bb4
# API docs here: https://documenter.getpostman.com/view/2568274/SzS8rjbe?version=latest#e629a11a-695c-4dab-8eff-5e0594735507




def lambda_handler(event, context):

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


    url = "https://covidapi.info/api/v1/country/"
    
    payload  = {}
    headers= {}
    
    api_csv = 'date, country, confirmed, deaths, recovered\n'
    
    
    for country in ['IRL', 'ITA', 'ESP', 'GBR', 'USA']:
        response = requests.request("GET", url + country, headers=headers, data = payload)
    
        y = json.loads(response.text.encode('utf8'))
        api_csv = dict_to_csv(csv = api_csv,
                              res_dict = y['result'],
                              country = country)

    
    
    # Make a file like object       
    file_obj = StringIO(api_csv)
    
    # Get the current datetime for the file name
    now = str(datetime.today())
    	
    # Export the data to S3
    #client = boto3.client('s3')
    
    #response = client.put_object(Bucket='c19datastore',
    #                             Body=file_obj, 
    #                             Key='rawdata/{}.csv'.format(now))
    
    s3_resource = boto3.resource('s3')
    
    s3_resource.Object('c19datastore',
                       'rawdata/{}.csv'.format(now)).put(Body=file_obj.getvalue())


