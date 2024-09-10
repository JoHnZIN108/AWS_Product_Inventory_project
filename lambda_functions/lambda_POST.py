import json
import os
from aws_cdk import boto3

# initilize dynamodb
region = os.environ['AWS_REGION']

dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table('Products_Table')


def lambda_handler(event, context):

    try: 
        # Parse the event body as JSON
        body = json.loads(event['body'])

    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid request body')
        }

    # Verifying required fields 
    required_fields = ['productid', 'productname', 'category', 'price', 'quantity']
    
    for field in required_fields:
        if field not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": f"Missing required field: {field}"})
            }
    
    # Extract the prameters from the event body

    try:
        response = table.put_item(
            Item={
                'Product ID': body['productid'], 
                'Product Name': body['productname'],
                'Category': body['category'],
                'Price': body['price'],
                'Quantity': body['quantity']
            }
        )

        return{
            'statusCode': 200,
            'body': json.dumps('Product added successfully!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error adding product: {str(e)}')
        }
        

