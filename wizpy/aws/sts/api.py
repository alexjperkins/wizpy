from typing import Optional

from aws.sts.service import STSService
from wizard import register_wizard


@register_wizard
class STSAPI:
    """STS: All things account(s) & identity as provided by aws."""
    @staticmethod
    def get_account_id() -> Optional[str]:
        """
            Retrieves the aws account id from the defined aws credentials.
        """
        return STSService.get_caller_identity().get('Account', None)
