from typing import List

from aws.sagemaker.client import SageMakerClient


class SageMakerService:

    client = SageMakerClient.client

    @classmethod
    def create_model(
        cls,
        *,
        model_name: str,
        primary_container_config: dict,
        execution_role_arn: str,
        vpc_config: dict,
    ) -> dict:

        return cls.client.create_model(
            ModelName=model_name,
            PrimaryContainer=primary_container_config,
            ExecutionRoleArn=execution_role_arn,
            VpcConfig=vpc_config,
            Tags=[{"Key": "CreationMethod", "Value": "Scripted"}],
            EnableNetworkIsolation=False
        )

    @classmethod
    def create_endpoint_config(
        cls,
        *,
        endpoint_config_name: str,
        production_variants: List[dict]
    ) -> dict:

        return cls.client.create_endpoint_config(
            EndpointConfigName=endpoint_config_name,
            ProductionVariants=production_variants,
            Tags=[{"Key": "CreationMethod", "Value": "Scripted"}],
        )

    @classmethod
    def create_endpoint(
        cls,
        *,
        endpoint_name: str,
        endpoint_config_name: str,
    ) -> dict:

        return cls.client.create_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=endpoint_config_name,
            Tags=[{"Key": "CreationMethod", "Value": "Scripted"}],
        )

    @classmethod
    def update_existing_endpoint(
        cls,
        *,
        endpoint_name: str,
        endpoint_config_name: str,
    ) -> dict:

        return cls.client.update_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=endpoint_config_name,
            RetainAllVariantProperties=True,
        )

    @classmethod
    def list_endpoint_configs(cls, *, name_contains=None) -> dict:
        attrs = {
            "NameContains": str(name_contains),
        } if name_contains else {}

        return cls.client.list_endpoint_configs(
            **attrs
        )

    @staticmethod
    def format_endpoint_config_name_from_model(*, model_name: str) -> str:
        return f"{model_name}-endpoint-config".replace('/', '-')

    @staticmethod
    def format_endpoint_name_from_model(*, model_name: str) -> str:
        return f"{model_name}-endpoint".replace('/', '-')
