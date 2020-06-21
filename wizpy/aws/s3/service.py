import logging

from botocore.client import ClientError

from aws.s3.client import S3Client
from aws.s3.util import (
    append_extension_to_filename, does_name_match_bucket,
)

logger = logging.getLogger(__file__)


class S3Service:

    client = S3Client.client

    @classmethod
    def create_bucket(cls, *, bucket, access: str, region: str) -> dict:
        try:
            return cls.client.create_bucket(
                Bucket=bucket,
                ACL=access,
                region=region,
            )
        except ClientError as error:
            logger.error(error)
            raise

    @classmethod
    def list_buckets(cls) -> dict:
        return cls.client.list_bucket()

    @classmethod
    def does_bucket_exist(cls, *, bucket_name: str) -> dict:
        buckets = cls.list_buckets()
        return (
            any(
                does_name_match_bucket(bucket=bucket, name_to_match=bucket_name)  # NOQA
                for bucket in buckets['Buckets']
            )
        )

    @classmethod
    def put_bucket_event(cls, *, bucket: str, config: dict) -> dict:
        return cls.client.put_bucket_notification_configuration(
            Bucket=bucket,
            NotificationConfiguration=config
        )

    @classmethod
    def get_current_bucket_event(cls, *, bucket: str) -> dict:
        return cls.client.get_bucket_notification_configuration(
            bucket=bucket
        )

    @classmethod
    def upload_model(cls, *, file_name: str, bucket: str, object_name: str):

        filename_with_extension = append_extension_to_filename(
            file_name=file_name,
        )

        return cls.client.upload_file(
            Filename=filename_with_extension,
            Bucket=bucket,
            Key=object_name,
            ExtraArgs={'ACL': 'public-read'},
        )

    @staticmethod
    def format_s3_url_from_bucket_and_key(*, bucket: str, key: str) -> str:
        return (
            f"https://{bucket}.s3.eu-west-2"
            f".amazonaws.com/{key}"
        )
