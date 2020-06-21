import logging
from typing import Dict, List, Optional

from aws.ec2.services import EC2Service
from wizard import register_wizard


logger = logging.getLogger(__file__)


class MissingVPCError(Exception):
    pass


@register_wizard
class EC2API:
    """EC2: Manage EC2 Containers, VPCs and more."""
    @staticmethod
    def get_vpc_id(*, is_default: bool = False) -> str:
        """
            Retrieves the VPC id (either default or otherwise).
        """
        vpcs = EC2Service.describe_vpcs_by_default_filter(
            is_default=is_default
        )['Vpcs']

        if not vpcs:
            raise MissingVPCError(
                f'Cannot retrieve VPC ID: '
                f'filter: ``is_default: {is_default}``'
            )

        if len(vpcs) > 1:
            logger.warning(
                'More than one VPC found, retrieving ID for the first '
                'from:\n %s', vpcs
            )

        return vpcs[0]['VpcId']

    @staticmethod
    def list_subnet_ids(
        *, filters: Optional[List[Dict]] = None
    ) -> List[str]:
        """
            Lists all subnet ids.
        """

        subnets = EC2Service.describe_subnets(
            filters=filters
        )

        return [subnet['SubnetId'] for subnet in subnets.get('Subnets', [])]
