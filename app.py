#!/usr/bin/env python3

import aws_cdk as cdk
from product_project.lambda_stack import LambdaStack
from product_project.s3_bucket_stack import S3BucketStack
from product_project.dynamodb_stack import DynamoDBStack
from product_project.api_stack import APIStack

app = cdk.App()

# S3 bucket stack
s3_stack = S3BucketStack(app, "S3BucketStack")

# DynamoDB stack
api_dynamo_stack = DynamoDBStack(app, "DynamoDBStack")

# Lambda stack with DynamoDB table
lambda_stack = LambdaStack(
    app,
    "LambdaStack",
    dynamodb_table=api_dynamo_stack.DB_table  # Pass the DynamoDB table from APIDynamoDBStack
)

# API stack, passing lambda stack to it
api_stack = APIStack(
    app,
    "APIStack",
    lambda_stack=lambda_stack, # Pass the Lambda stack to the API stack
)

app.synth()
