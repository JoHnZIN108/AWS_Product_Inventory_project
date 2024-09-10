import json
import os
from aws_cdk import boto3

# Initialize DynamoDB
region = os.environ['AWS_REGION']
dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table('Products_Table')

def lambda_handler(event, context):
    # Get productid from the path parameters
    product_id = event['pathParameters']['productid']

    try:
        # Parse the request body
        body = json.loads(event['body'])
        
        # Extract the parameters
        productname = body.get('productname')
        category = body.get('category')
        price = body.get('price')
        quantity = body.get('quantity')

        # Update the table
        response = table.update_item(
            Key={
                'Product ID': product_id  # Use the correct partition key
            },
            UpdateExpression='SET Product Name = :n, Category = :c, Price = :p, Quantity = :q',
            ExpressionAttributeValues={
                ':n': productname,
                ':c': category,
                ':p': price,
                ':q': quantity
            },
            ReturnValues='UPDATED_NEW'  # Optionally return updated attributes
        )

        # Return a success response
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Product {product_id} updated successfully'})
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
