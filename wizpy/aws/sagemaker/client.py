from aws import AbstractAWSClient


class SageMakerClient(AbstractAWSClient):
    _service = 'sagemaker'
