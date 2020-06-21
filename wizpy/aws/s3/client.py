from aws import AbstractAWSClient


class S3Client(AbstractAWSClient):
    _service = 's3'
