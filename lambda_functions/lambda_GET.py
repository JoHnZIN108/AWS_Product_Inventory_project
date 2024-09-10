import json
from aws_cdk import boto3
import os

# Get region from environment variable
region = os.environ['AWS_REGION']

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table('Products_Table')

def lambda_handler(event, context):
    try:
        if event['httpMethod'] != 'GET':
            return {
                'statusCode': 405,
                'body': json.dumps('Method Not Allowed')
            }
        
        print('HTTP GET Request Received', event)
        
        response = table.scan()
        data = response['Items']
        
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        
        return {
            'statusCode': 200,
            'body': json.dumps(data)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }


