import json
import os
from aws_cdk import boto3

# initilize dynamodb
region = os.environ['AWS_REGION']

dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table('Products_Table')


def lambda_handler(event, context):

    # Get the product id from the path parameters
    product_id = event['pathParameters']['id']

    try:
        # Retrieve the product from the database
        response = table.delete_item(
            Key={'Product ID': product_id},
            condition_expression='attribute_exists(Product ID)' # To ensure the product exists
            )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message':f'Product {product_id} deleted Successfully!'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error deleting product: {str(e)}')
        }