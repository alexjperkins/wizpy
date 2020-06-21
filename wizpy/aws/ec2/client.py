from aws import AbstractAWSClient


class EC2Client(AbstractAWSClient):
    _service = 'ec2'
