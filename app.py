#!/usr/bin/env python3
import os

import aws_cdk as cdk
from docker_cdk.docker_cdk_stack import DockerCdkStack


app = cdk.App()
core_env = cdk.Environment(region="ap-northeast-2")
DockerCdkStack(app, "DockerCdkStack", env=core_env)

app.synth()
