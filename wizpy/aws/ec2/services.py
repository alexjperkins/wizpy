from typing import Dict, List, Optional

from aws.ec2.client import EC2Client


class EC2Service:

    client = EC2Client.client

    @classmethod
    def describe_vpcs_by_filter(
            cls, *, filters: Optional[List[Dict]] = None
    ) -> dict:

        return cls.client.describe_vpcs(
            Filters=filters or list()
        )

    @classmethod
    def describe_vpcs_by_default_filter(cls, is_default: bool = False) -> dict:
        return cls.describe_vpcs_by_filter(
            filters=[
                {
                    'Name': 'isDefault',
                    'Values': [
                        'true'
                    ]
                }
            ]
        )

    @classmethod
    def describe_subnets(
            cls, *, filters: Optional[List[Dict]] = None
    ) -> dict:

        return cls.client.describe_subnets(
            Filters=filters or list()
        )
