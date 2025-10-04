import logging

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from app.bootstrap.configs import (
    ApiConfig,
    Config,
    PostgresConfig,
)
from app.bootstrap.ioc.application import ApplicationProvider
from app.bootstrap.ioc.config import AppSetupProvider
from app.bootstrap.ioc.infrastructure import InfrastructureProvider

logger = logging.getLogger(__name__)


def fastapi_container(
        config: Config,
) -> AsyncContainer:
    logger.info("Fastapi DI setup")

    return make_async_container(
        AppSetupProvider(),
        ApplicationProvider(),
        InfrastructureProvider(),
        FastapiProvider(),
        context={
            PostgresConfig: config.database,
            ApiConfig: config.api,
        },
    )
