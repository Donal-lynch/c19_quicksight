import json
from datetime import datetime
#import os
import boto3

# Code adaapted from: https://github.com/scochran3/data_acquisition_aws_lambda/blob/master/lambda_function.py
# Tutorial is here: https://towardsdatascience.com/make-data-acquisition-easy-with-aws-lambda-python-in-12-steps-33fe201d1bb4

def lambda_handler(event, context):