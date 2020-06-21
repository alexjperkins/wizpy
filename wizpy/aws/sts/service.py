from typing import Optional

from aws.sts.client import STSClient


class STSService:

    client = STSClient.client

    @classmethod
    def get_caller_identity(cls) -> dict:
        return cls.client.get_caller_identity()
