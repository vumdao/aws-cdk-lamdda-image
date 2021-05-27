from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam
)
import os


class DockerCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, env, **kwargs) -> None:
        super().__init__(scope, construct_id, env=env, **kwargs)

        policy_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "logs:CreateLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents"
            ],
            resources=['arn:aws:logs:*:*:*'],
            conditions={'StringEquals': {"aws:RequestedRegion": "ap-northeast-2"}}
        )
        lambda_role = iam.Role(self, 'LambdaRole', assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                               role_name='docker-cdk-role')
        lambda_role.add_to_policy(statement=policy_statement)
        lambda_image = _lambda.DockerImageFunction(
            self, 'DockerImageFunc',
            function_name='docker-aws-cdk',
            code=_lambda.DockerImageCode.from_image_asset(
                directory=f'{os.getcwd()}/resource', file='Dockerfile', exclude=['cdk.out'],
            ),
            role=lambda_role
        )
