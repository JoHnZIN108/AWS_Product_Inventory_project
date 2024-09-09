#!/usr/bin/env python3

import aws_cdk as cdk

from product_project.product_project_stack import ProductProjectStack


app = cdk.App()
ProductProjectStack(app, "ProductProjectStack")

app.synth()
