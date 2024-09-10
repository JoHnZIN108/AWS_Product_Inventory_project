import aws_cdk as core
import aws_cdk.assertions as assertions
from product_project.lambda_stack import lambdaStack


def test_lambda_function_created():
    app = core.App()
    stack = lambdaStack(app, "product-lambda-stack")
    template = assertions.Template.from_stack(stack)

    # Check if a Lambda function is created
    template.resource_count_is("AWS::Lambda::Function", 4)

    # Optionally, check properties of a Lambda function (example: runtime)
    template.has_resource_properties("AWS::Lambda::Function", {
        "Runtime": "python3.10"
    })