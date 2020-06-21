from aws import AbstractAWSClient


class ECRClient(AbstractAWSClient):
    _service = 'ecr'
