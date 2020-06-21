import logging

from botocore.client import ClientError

from aws.s3.service import S3Service
from wizard import register_wizard


logger = logging.getLogger(__file__)


@register_wizard(definition=["create_bucket", "toggle_bucket_lambda_event"])
class S3API:
    """S3: S3 API for AWS."""
    @staticmethod
    def create_bucket(
        *, bucket: str, access='private', region='eu-west-2'
    ) -> dict:
        """
            Creates a bucket in S3.
        """
        S3Service.create_bucket(
            bucket=bucket,
            access=access,
            region=region,
        )

    @classmethod
    def toggle_bucket_lambda_event(
        cls, *, bucket, config: dict, create_bucket_if_not_exist=False
    ) -> dict:
        """
            Toggles and event on an S3 Bucket.
        """
        if (
                create_bucket_if_not_exist and not
                S3Service.does_bucket_exist(bucket_name=bucket)
        ):
            cls.create_bucket(bucket=bucket)

        current_event = S3Service.get_current_bucket_event(bucket=bucket)
        lambdas =current_event.get('LambdaFunctionConfigurations')

        if len(lambdas) > 1:
            logger.warn(
                'WARNING: There are currently more than one lambda'
                ' defined on this bucket, toggling the first event'
            )
        try:
            if lambdas[0] == config:
                no_event = {}
                S3Service.put_bucket_event(bucket=bucket, config=no_event)
                return {
                    "success": True,
                    "config": no_event
                }

            S3Service.put_bucket_event(bucket=bucket, config=config)
            return {
                "success": True,
                "config": config
            }

        except ClientError as error:
            logger.error(error)
            return {
                "success": False,
                "config": {}
            }

    @staticmethod
    def upload_model(*, file_name: str, bucket: str, object_name: str):
        """
            Uploads a model to S3 given a local tarbell.
        """
        return S3Service.upload_model(
            file_name=file_name,
            bucket=bucket,
            object_name=object_name,
        )

    @staticmethod
    def format_s3_url_from_bucket_and_key(*, bucket: str, key: str) -> str:
        return S3Service.format_s3_url_from_bucket_and_key(
            bucket=bucket,
            key=key
        )
