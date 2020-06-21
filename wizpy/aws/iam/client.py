from aws import AbstractAWSClient


class IAMClient(AbstractAWSClient):
    _service = 'iam'
