from fastapi.security.api_key import APIKeyHeader
from fastapi import Security
from app.exceptions import AppError
from os import environ

API_KEYS = environ["API_KEYS"].split(",")
api_key_header = APIKeyHeader(name="access_token", auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key in API_KEYS:
        return api_key_header
    else:
        raise AppError.INVALID_API_KEY_ERROR
