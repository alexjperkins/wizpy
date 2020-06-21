from aws.ecr.interfaces import STSInterface
from aws.ecr.util import ecr_image_uri_factory

from wizard import register_wizard


@register_wizard
class ECRAPI:
    """ECR: The AWS Elastic Container Registry."""
    @staticmethod
    def get_image_uri_from_model_name(
        *, model_name: str, region: str='eu-west-2'
    ) -> str:
        """
            Retrieves the `URI` for a given imagine by model name
        """
        account_id = STSInterface.get_account_id()

        return ecr_image_uri_factory(
            account_id=account_id,
            model_name=model_name,
            region=region
        )
