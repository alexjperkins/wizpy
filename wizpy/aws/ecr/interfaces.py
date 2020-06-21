from typing import Optional

from aws.sts.api import STSAPI


class STSInterface:
    @staticmethod
    def get_account_id() -> Optional[str]:
        return STSAPI.get_account_id()
