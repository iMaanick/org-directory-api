from dishka import Provider, Scope, from_context

from app.bootstrap.configs import (
    PostgresConfig,
)


class AppSetupProvider(Provider):
    scope = Scope.APP

    database_config = from_context(PostgresConfig)
