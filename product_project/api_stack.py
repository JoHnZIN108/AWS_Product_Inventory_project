from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
    aws_apigateway as apigateway,
    aws_cloudfront_origins as origins,
    aws_cloudfront as cloudfront,
    aws_iam as iam,
)
from constructs import Construct

class APIStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, lambda_stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Create API Gateway
        API = apigateway.RestApi(
            self, "ProductAPI",
            default_cors_preflight_options={
                "allow_origins": apigateway.Cors.ALL_ORIGINS,
                "allow_methods": apigateway.Cors.ALL_METHODS,
            }
        )

        # Define lambda integration with API Gateway
        GET_integration = apigateway.LambdaIntegration(lambda_stack.GET_function)
        POST_integration = apigateway.LambdaIntegration(lambda_stack.POST_function)
        UPDATE_integration = apigateway.LambdaIntegration(lambda_stack.UPDATE_function)
        DELETE_integration = apigateway.LambdaIntegration(lambda_stack.DELETE_function)

        # Create API resources
        products = API.root.add_resource("products")
        products.add_method("GET", GET_integration)
        products.add_method("POST", POST_integration)

        product = products.add_resource("{product_id}")
        product.add_method("GET", GET_integration)
        product.add_method("PUT", UPDATE_integration)
        product.add_method("DELETE", DELETE_integration)

        # Output API Gateway URL
        CfnOutput(self, "API_URL", value=API.url_for_path("/products"))
