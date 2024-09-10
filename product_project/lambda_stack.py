from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
)


class LambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, dynamodb_table:dynamodb.ITableV2 , **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Lambda Functions
        self.GET_function = lambda_.Function(
            self, "GETFunction",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="lambda_GET.lambda_handler", # Filename and function name
            code=lambda_.Code.from_asset("lambda_functions"), # code loaded from lambda_function folder
            environment={
                "TABLE_NAME": dynamodb_table.table_name
            }
        )

        self.POST_function = lambda_.Function(
            self, "POSTFunction",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="lambda_POST.lambda_handler",
            code=lambda_.Code.from_asset("lambda_functions"),
            environment={
                "TABLE_NAME": dynamodb_table.table_name
            }
        )

        self.UPDATE_function = lambda_.Function(
            self, "UPDATEFunction",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="lambda_UPDATE.lambda_handler",
            code=lambda_.Code.from_asset("lambda_functions"),
            environment={
                "TABLE_NAME": dynamodb_table.table_name
            }
            
        )

        self.DELETE_function = lambda_.Function(
            self, "DELETEFunction",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="lambda_DELETE.lambda_handler",
            code=lambda_.Code.from_asset("lambda_functions"),
            environment={
                "TABLE_NAME": dynamodb_table.table_name
            }
        )

        # Adding permissions to Lambda functions
        dynamodb_table.grant_read_data(self.GET_function)
        dynamodb_table.grant_read_write_data(self.POST_function)
        dynamodb_table.grant_read_write_data(self.UPDATE_function)
        dynamodb_table.grant_read_write_data(self.DELETE_function)