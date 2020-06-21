from typing import Dict, List, Optional

from aws.ec2.api import EC2API
from aws.ecr.api import ECRAPI
from aws.iam.api import IAMAPI
from aws.s3.api import S3API


class EC2Interface:
    @staticmethod
    def get_vpc_id(*, is_default: bool = False) -> str:
        return EC2API.get_vpc_id(
            is_default=is_default
        )

    @staticmethod
    def list_subnet_ids(*, filters: Optional[List[Dict]] = None) -> List[str]:
        return EC2API.list_subnet_ids(
            filters=filters
        )


class ECRInterface:
    @staticmethod
    def get_image_uri_from_model_name(
        *, model_name: str,
    ) -> str:
        return ECRAPI.get_image_uri_from_model_name(
            model_name=model_name
        )


class IAMInterface:
    @staticmethod
    def get_role_arn(*, role_name_to_match='SageMakerExecutionRole') -> str:
        return IAMAPI.get_role_arn(
            role_name_to_match=role_name_to_match
        )


class S3Interface:
    @staticmethod
    def upload_model(*, file_name: str, bucket: str, object_name: str):
        return S3API.upload_model(
            file_name=file_name,
            bucket=bucket,
            object_name=object_name
        )

    @staticmethod
    def format_s3_url_from_bucket_and_key(*, bucket: str, key: str) -> str:
        return S3API.format_s3_url_from_bucket_and_key(
            bucket=bucket,
            key=key
        )
