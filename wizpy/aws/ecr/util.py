def ecr_image_uri_factory(
    *, account_id: str, model_name: str, region: str
) -> str:
    return (
        f'{account_id}.dkr.ecr.{region}.amazonaws.com/{model_name}'
    )
