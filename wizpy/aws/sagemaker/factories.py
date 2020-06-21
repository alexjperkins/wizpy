from typing import List


def sagemaker_container_kwargs_factory(
    *,
    s3_model_artifact_uri: str,
    ecr_image_uri: str,
    mode: str = 'SingleMode',
    **kwargs
) -> dict:
    return {
        "ModelDataUrl": s3_model_artifact_uri,
        "Image": ecr_image_uri,
        "Mode": mode,
        **kwargs
    }


def sagemaker_vpc_kwargs_factory(
    *, security_group_ids: List[str], subnet_ids: List[str], **kwargs
) -> dict:
    return {
        "SecurityGroupIds": security_group_ids,
        "Subnets": subnet_ids,
        **kwargs
    }


def sagemaker_variant_kwargs_factory(
    *,
    variant_name: str, instance_count: int, instance_type: str, model_name: str, **kwargs
) -> dict:
    return {
        "VariantName": variant_name,
        "InitialInstanceCount": instance_count,
        "InstanceType": instance_type,
        "ModelName": model_name,
        **kwargs
    }
