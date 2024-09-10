from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
    aws_apigateway as apigateway,

)
from constructs import Construct
from aws_cdk.aws_dynamodb import (
    AttributeType,
    TableV2,
)
from aws_cdk.aws_apigateway import (
    Cors,
    LambdaIntegration,
    RestApi,
    ApiKeySourceType,
    ApiKey,
)

class APIStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, lambda_stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

 
        # Create API Gateway
        API = RestApi(
            self, "ProductAPI",
            default_cors_preflight_options={
                "allow_origins": apigateway.Cors.ALL_ORIGINS,
                "allow_methods": apigateway.Cors.ALL_METHODS,
            }
        )

        # Define lambda integration with API Gateway
        GET_integration = LambdaIntegration(lambda_stack.GET_function)    
        POST_integration = LambdaIntegration(lambda_stack.POST_function)
        UPDATE_integration = LambdaIntegration(lambda_stack.UPDATE_function)
        DELETE_integration = LambdaIntegration(lambda_stack.DELETE_function)  

        # Create API resources
        products = API.root.add_resource("products")
        products.add_method("GET", GET_integration)
        products.add_method("POST", POST_integration)

        product = products.add_resource("{product_id}")
        product.add_method("GET", GET_integration)
        product.add_method("PUT", UPDATE_integration)
        product.add_method("DELETE", DELETE_integration)

        # Output API URL
        CfnOutput(self, "API_URL", value=API.url_for_path("/products"))
  
   

        