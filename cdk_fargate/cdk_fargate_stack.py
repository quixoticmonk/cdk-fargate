from aws_cdk import core as cdk
from aws_cdk import aws_ecs as ecs, aws_ec2 as ec2, aws_elasticloadbalancingv2 as elbv2


class CdkFargateStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, vpc_id: ec2.Vpc.vpc_id, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        _vpc = ec2.Vpc.from_lookup(
            self,
            "vpc",
            is_default=True
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

        _container = _task_def.add_container(
            "taskcontainer",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
        )
        _container.add_port_mappings(ecs.PortMapping(container_port=3000, protocol=ecs.Protocol.TCP))

        service = ecs.FargateService(
            self,
            "fargateservuce",
            cluster=_cluster,
            task_definition=_task_def,
            desired_count=1
        )

        lb = elbv2.ApplicationLoadBalancer(self, "LB", vpc=_vpc, internet_facing=True)

        listener = lb.add_listener("Listener", port=80)

        target_group = listener.add_targets(
            "fargateTarget",
            port=80,
            targets=[service]
        )
