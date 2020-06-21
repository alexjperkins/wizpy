from aws import AbstractAWSClient


class STSClient(AbstractAWSClient):
    _service = 'sts'
