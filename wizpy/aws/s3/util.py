def append_extension_to_filename(*, file_name: str, extension: str = "bin"):
    return f"{file_name}.{extension}"


def does_name_match_bucket(*, bucket: dict, name_to_match: str) -> bool:
    return bucket.get("Name") == name_to_match
