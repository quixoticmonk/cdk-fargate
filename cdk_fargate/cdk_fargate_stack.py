from aws_cdk import core as cdk
from aws_cdk import aws_ecs as ecs, aws_ec2 as ec2


class CdkFargateStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, vpc_id: ec2.Vpc.vpc_id, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        _vpc = ec2.Vpc.from_lookup(
            self,
            "vpc",
            vpc_id=vpc_id
        )

        _cluster = ecs.Cluster(
            self,
            "ecscluster",
            vpc=_vpc
        )

        _task_def = ecs.FargateTaskDefinition(
            self,
            "fargatetask",
            memory_limit_mib=512,
            cpu=256
        )

        _task_def.add_container(
            "taskcontainer",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
        )

        ecs.FargateService(
            self,
            "fargateservuce",
            cluster=_cluster,
            task_definition=_task_def,
            desired_count=5
        )
