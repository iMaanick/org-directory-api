import logging
from collections.abc import AsyncIterable, AsyncIterator

from dishka import Provider, Scope, provide
from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.application.common.ports.uow import UoW
from app.bootstrap.configs import ApiConfig, PostgresConfig
from app.infrastructure.auth.api_key_transport import ApiKeyTransport
from app.presentation.auth.static_api_key_validator import (
    StaticApiKeyValidator,
)

logger = logging.getLogger(__name__)


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    async def engine(
            self, config: PostgresConfig,
    ) -> AsyncIterator[AsyncEngine]:
        async_engine = create_async_engine(
            url=config.uri,
            echo=False,
            pool_size=15,
            max_overflow=5,
            connect_args={"connect_timeout": 5},
            pool_pre_ping=True,
        )
        yield async_engine
        await async_engine.dispose()

    @provide(scope=Scope.APP)
    def get_sessionmaker(
            self, engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        factory = async_sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autoflush=False,
        )
        logger.info("Session provider was initialized")
        return factory

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self, factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with factory() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_api_key_transport(
            self, config: ApiConfig, request: Request,
    ) -> ApiKeyTransport:
        return StaticApiKeyValidator(config.api_key, request)

    @provide(scope=Scope.REQUEST)
    async def get_uow(
            self, session: AsyncSession,
    ) -> UoW:
        return session
