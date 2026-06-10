from fastapi import Header


def get_model_api_key(
    x_model_api_key: str | None = Header(default=None),
) -> str | None:
    return x_model_api_key
