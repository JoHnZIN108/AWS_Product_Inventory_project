from aws_cdk import Stack, RemovalPolicy
from constructs import Construct
from aws_cdk.aws_dynamodb import AttributeType, TableV2

class DynamoDBStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create DynamoDB Table
        self.DB_table = TableV2(
            self, "ProductTable",
            table_name="Products_Table",
            partition_key={"name": "Product ID", "type": AttributeType.STRING},
            sort_key={"name": "Product Name", "type": AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY
        )