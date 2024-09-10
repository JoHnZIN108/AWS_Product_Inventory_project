from constructs import Construct
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    CfnOutput,
    aws_cloudfront_origins as origins,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3_deployment as s3_deployment,
)

class S3BucketStack(Stack):
    
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        self.website_bucket = s3.Bucket(
            self, "WebsiteBucket",
            website_index_document="index.html",
            website_error_document="error.html",
        )

        # Deploy website files to s3 Bucket
        s3_deployment.BucketDeployment(
            self, "DeployWebsite",
            sources=[s3_deployment.Source.asset("./website")],
            destination_bucket=self.website_bucket
        )

        # CloudFront distribution for the S3 bucket
        distribution = cloudfront.Distribution(
            self, "WebsiteDistribution",
            default_behavior={
                "origin": origins.S3Origin(self.website_bucket),
                "viewer_protocol_policy": cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            },
            default_root_object="index.html",
        )

        # Output the CloudFront URL
        CfnOutput(
            self, "DistributionDomainName",
            value=distribution.distribution_domain_name,
            description="CloudFront distribution domain name.",
        )
        
