<p align="center">
  <a href="https://dev.to/vumdao">
    <img alt="Quick Start Lambda Container Image Using AWS CDK" src="https://github.com/vumdao/aws-cdk-lamdda-image/blob/master/image/cover.jpg?raw=true" width="700" />
  </a>
</p>
<h1 align="center">
  <div><b>Quick Start Lambda Container Image Using AWS CDK 2.0</b></div>
</h1>

### - This post create a lambda function container image to send a message to Slack using IaC - AWS CDK 2.0, use this as a quick guide for your practice of those keywords.

---

## Whatโs In This Document
- [Lambda function handler](#-Lambda-function-handler)
- [Dockerfile base on AWS lambda image](#-Dockerfile-base-on-AWS-lambda-image)
- [CDK stack](#-CDK-stack)
- [Invoke lambda function](#-Invoke-lambda-function)

---

### ๐ **[Lambda function handler](#-Lambda-function-handler)**
- You need a slack webhook url of the registered channel to send messages to

```
#!/usr/bin/env python
from datetime import datetime
import json
import requests


def handler(event, context):
    webhook_url = 'https://hooks.slack.com/services/WORKSPACE_ID/WEBHOOK_ID'
    footer_icon = 'https://static.io/img/cdk.png'
    color = '#36C5F0'
    level = ':white_check_mark: INFO :white_check_mark:'
    curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = event['msg']
    slack_payload = {"username": "From-Lambda-Image",
                     "attachments": [{"fallback": "Required plain-text summary of the attachment.",
                                      "pretext": level,
                                      "color": color,
                                      "text": message,
                                      "footer": curr_time,
                                      "footer_icon": footer_icon}]}
    requests.post(webhook_url, data=json.dumps(slack_payload), headers={'Content-Type': 'application/json'})
```

### ๐ **[Dockerfile base on AWS lambda image](#-Dockerfile-base-on-AWS-lambda-image)**
- Dockerfile should use aws-lambda-* as a base image in order to have lambda API

```
FROM amazon/aws-lambda-python:3.8

RUN yum -y update && \
    yum install -y python3-pip && \
    pip3 install requests

COPY app.py ./

CMD ["app.handler"]
```

### ๐ **[CDK stack](#-CDK-stack)**
- Stack will create
  - IAM role for writing cloudwatch log
  - Build image and then push to ECR
  - Lambda function container image

```
โก $ tree
.
โโโ app.py
โโโ docker_cdk
โย?ย? โโโ docker_cdk_stack.py
โย?ย? โโโ __init__.py
โย?ย? โโโ __pycache__
โย?ย?     โโโ docker_cdk_stack.cpython-38.pyc
โย?ย?     โโโ __init__.cpython-38.pyc
โโโ requirements.txt
โโโ resource
โย?ย? โโโ app.py
โย?ย? โโโ Dockerfile
โโโ setup.py
โโโ source.bat
```

```
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
```

### ๐ **[Invoke lambda function](#-Invoke-lambda-function)**
```
โก $ aws lambda invoke --function-name docker-aws-cdk --region ap-northeast-2 --payload '{"msg":"Hello"}' --cli-binary-format raw-in-base64-out outfile
{
    "StatusCode": 200,
    "ExecutedVersion": "$LATEST"
}
โก $ aws lambda invoke --function-name docker-aws-cdk --region ap-northeast-2 --payload '{"msg":"How are you?"}' --cli-binary-format raw-in-base64-out outfile
{
    "StatusCode": 200,
    "ExecutedVersion": "$LATEST"
}
```

![Alt-Text](https://github.com/vumdao/aws-cdk-lamdda-image/blob/master/image/test.png?raw=true)
---

<h3 align="center">
  <a href="https://dev.to/vumdao">:stars: Blog</a>
  <span> ยท </span>
  <a href="https://github.com/vumdao/aws-cdk-lamdda-image">Github</a>
  <span> ยท </span>
  <a href="https://stackoverflow.com/users/11430272/vumdao">stackoverflow</a>
  <span> ยท </span>
  <a href="https://www.linkedin.com/in/vu-dao-9280ab43/">Linkedin</a>
  <span> ยท </span>
  <a href="https://www.linkedin.com/groups/12488649/">Group</a>
  <span> ยท </span>
  <a href="https://www.facebook.com/CloudOpz-104917804863956">Page</a>
  <span> ยท </span>
  <a href="https://twitter.com/VuDao81124667">Twitter :stars:</a>
</h3>

