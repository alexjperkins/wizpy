from aws.sagemaker.service import SageMakerService
from aws.sagemaker.interfaces import (
    EC2Interface, ECRInterface, IAMInterface, S3Interface
)
from aws.sagemaker.factories import (
    sagemaker_container_kwargs_factory,
    sagemaker_vpc_kwargs_factory,
    sagemaker_variant_kwargs_factory,
)

from wizard import register_wizard


@register_wizard
class SageMakerAPI:
    """Sagemaker: Machine Learning Service as provided by aws."""

    @classmethod
    def upload_artifact_and_create_model(
        cls,
        local_model_path: str,
        model_bucket_name: str,
        model_name: str,
        use_default_vpc: bool,
    ) -> dict:
        """
            Uploads artifact to s3 and and create model in Sagemaker.
        """
        # upload model to s3
        S3Interface.upload_model(
            file_name=local_model_path,
            bucket=model_bucket_name,
            object_name=model_name
        )

        # create model in sagemaker
        s3_model_artifact_uri = S3Interface.format_s3_url_from_bucket_and_key(
            bucket=model_bucket_name,
            key=model_name
        )

        ecr_image_uri = ECRInterface.get_image_uri_from_model_name(
            model_name=model_name
        )

        container_config = sagemaker_container_kwargs_factory(
            s3_model_artifact_uri=s3_model_artifact_uri,
            ecr_image_uri=ecr_image_uri
        )

        vpc_id = EC2Interface.get_vpc_id(
            is_default=use_default_vpc
        )

        subnet_ids = EC2Interface.list_subnet_ids()

        vpc_config = sagemaker_vpc_kwargs_factory(
            security_group_ids=[vpc_id],
            subnet_ids=subnet_ids
        )

        execution_role_arn = IAMInterface.get_role_arn()

        return SageMakerService.create_model(
            model_name=model_name,
            primary_container_config=container_config,
            execution_role_arn=execution_role_arn,
            vpc_config=vpc_config,
        )

    @classmethod
    def create_model_and_endpoint_config(
        cls,
        local_model_path: str,
        model_bucket_name: str,
        model_name: str,
        instance_count: int,
        instance_type: str,
        use_default_vpc: bool = False,
    ) -> dict:
        """
            Uploads model to S3
            Creates model in SageMaker
            Creates Endpoint Config in SageMaker
        """
        # create model
        model = cls.upload_artifact_and_create_model(
            local_model_path=local_model_path,
            model_bucket_name=model_bucket_name,
            model_name=model_name,
            use_default_vpc=use_default_vpc,
        )

        # create endpoint config
        endpoint_config_name = SageMakerService.format_endpoint_config_name_from_model(  # NOQA
            model_name=model_name
        )

        production_variants = [
            sagemaker_variant_kwargs_factory(
                variant_name=f'{model_name}-primary-variant',
                instance_count=instance_count,
                instance_type=instance_type,
                model_name=model_name
            ),
        ]

        endpoint_config = SageMakerService.create_endpoint_config(
            endpoint_config_name=endpoint_config_name,
            production_variants=production_variants,
        )

        return {
            "success": True,
            "model": model,
            "endpoint_config": endpoint_config,
        }

    @staticmethod
    def create_fullstack(
        local_model_path: str,
        model_bucket_name: str,
        model_name: str,
        instance_count: int,
        instance_type: str,
        use_default_vpc: bool = False,
    ) -> dict:
        """
            Uploads model to S3
            Creates model in Sagemaker
            Creates Endpoint Config in SageMaker
            Creates Enpoint in SagaMaker
        """
        # create model and endpoint
        model_and_endpoint_config = SageMakerAPI.create_model_and_endpoint_config(  # NOQA
            local_model_path=local_model_path,
            model_bucket_name=model_bucket_name,
            model_name=model_name,
            instance_count=instance_count,
            instance_type=instance_type,
            use_default_vpc=use_default_vpc,
        )

        # get endpoint config name
        endpoint_config_name = SageMakerService.format_endpoint_config_name_from_model(  # NOQA
            model_name=model_name
        )

        # create endpoint
        endpoint_name = SageMakerService.format_endpoint_name_from_model(
            model_name=model_name
        )

        endpoint = SageMakerService.create_endpoint(
            endpoint_name=endpoint_name,
            endpoint_config_name=endpoint_config_name,
        )

        return {
            **model_and_endpoint_config,
            "endpoint": endpoint,
            "success": True,
        }

    @staticmethod
    def create_endpoint(
        endpoint_name: str,
        endpoint_config_name: str
    ) -> dict:
        """
            Creates an endpoint (endpoint config must already exist.
        """
        return SageMakerService.create_endpoint(
            endpoint_name=endpoint_name,
            endpoint_config_name=endpoint_config_name,
        )

    @staticmethod
    def update_existing_endpoint(
        endpoint_name: str,
        endpoint_config_name: str,
    ) -> dict:
        """
            Updates a given endpoint (Switcheroo).
        """
        return SageMakerService.update_existing_endpoint(
            endpoint_name=endpoint_name,
            endpoint_config_name=endpoint_config_name,
        )

    @staticmethod
    def list_endpoint_configs(name_contains=None) -> dict:
        """
            Lists given endpoint configs.
        """
        return SageMakerService.list_endpoint_configs(
            name_contains=name_contains
        )
