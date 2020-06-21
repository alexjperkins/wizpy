import itertools

import os
from typing import List

import boto3


class MissingCredentials(Exception):
    pass


class AWSClientFactory:
    _required_creds = ('AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',)
    _other_creds = ('AWS_SESSION_TOKEN',)
    _region = "eu-west-2"
    _session = boto3.session.Session(region_name=_region)

    @classmethod
    def build(cls, service: str):
        credentials = {
            **cls._gather_environment(to_gather=cls._required_creds, raise_if_missing=True),
            **cls._gather_environment(to_gather=cls._other_creds),
        }

        return cls._session.client(
            service, region_name=cls._region, **credentials
        )

    @staticmethod
    def _gather_environment(
        *, to_gather: List, raise_if_missing=False
    ) -> dict:

        environment = [
            (key, value)
            for key in to_gather
            if (value := os.environ.get(key, None)) is not None
        ]

        if (raise_if_missing and len(environment) != len(to_gather)):
            raise MissingCredentials(
                f"Cannot find {to_gather} in your environment, please export.\n"
                f"More information can be found at: "
                f"`https://bitbucket.org/greenrunning/vcli/src/master/`"
            )

        return {
            key.lower(): value
            for key, value in environment
        }
