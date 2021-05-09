#!/usr/bin/env python3
import os

from aws_cdk import core

from cdk_fargate.cdk_fargate_stack import CdkFargateStack

_env = core.Environment(account="123456789",region="us-east-1")


app = core.App()
CdkFargateStack(app, "CdkFargateStack", "vpc-12345"
    )

app.synth()
