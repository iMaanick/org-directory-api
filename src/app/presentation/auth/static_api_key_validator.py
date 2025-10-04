import logging

from fastapi import Request

from app.application.common.exceptions.auth import (
    InvalidApiKeyError,
    MissingApiKeyError,
)
from app.infrastructure.auth.api_key_transport import ApiKeyTransport

logger = logging.getLogger(__name__)


class StaticApiKeyValidator(ApiKeyTransport):
    def __init__(self, static_api_key: str, request: Request) -> None:
        self.static_api_key = static_api_key
        self.header_name = "X-API-Key"
        self.request = request

    def validate(self) -> None:
        api_key = self.request.headers.get(self.header_name)

        if api_key is None:
            logger.info("API key not provided")
            raise MissingApiKeyError(self.header_name)

        if api_key != self.static_api_key:
            logger.info("Invalid API key provided")
            raise InvalidApiKeyError(self.header_name, api_key)

        logger.info("API key successfully validated")
