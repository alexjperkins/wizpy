from aws.iam.client import IAMClient


class IAMService:

    client = IAMClient.client

    @classmethod
    def get_role_arn(cls, *, role_name_to_match: str) -> str:
        role = cls.client.get_role(
            RoleName=role_name_to_match
        )
        return role['Role']['Arn']
