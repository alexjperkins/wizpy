from aws.iam.service import IAMService

from wizard import register_wizard


@register_wizard
class IAMAPI:
    """IAM: AWS roles and user manager."""
    @staticmethod
    def get_role_arn(*, role_name_to_match: str) -> str:
        """
            Retrieves the role ARN from a `search term`.
        """
        return IAMService.get_role_arn(
            role_name_to_match=role_name_to_match
        )
