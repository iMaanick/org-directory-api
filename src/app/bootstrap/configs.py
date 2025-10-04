from dataclasses import dataclass
from os import environ


class MissingPostgresConfigError(ValueError):
    def __init__(self) -> None:
        super().__init__(self.title)

    @property
    def title(self) -> str:
        return "Required postgres environment variables are missing"


@dataclass(frozen=True)
class PostgresConfig:
    host: str
    port: int
    db: str
    user: str
    password: str

    @property
    def uri(self) -> str:
        return (
            f"postgresql+psycopg://{self.user}:{self.password}@{self.host}"
            f":{self.port}/{self.db}"
        )


def load_postgres_config() -> PostgresConfig:
    host = environ.get("DB_HOST")
    port = environ.get("POSTGRES_PORT")
    db = environ.get("POSTGRES_DB")
    user = environ.get("POSTGRES_USER")
    password = environ.get("POSTGRES_PASSWORD")

    if (
            host is None
            or db is None
            or port is None
            or user is None
            or password is None
    ):
        raise MissingPostgresConfigError

    return PostgresConfig(
        host=host,
        port=int(port),
        db=db,
        user=user,
        password=password,
    )


class MissingApiConfigError(ValueError):
    def __init__(self) -> None:
        super().__init__(self.title)

    @property
    def title(self) -> str:
        return "Required Api environment variables are missing"


@dataclass(frozen=True)
class ApiConfig:
    api_key: str


def load_api_config() -> ApiConfig:
    api_key = environ.get("API_KEY")

    if api_key is None:
        raise MissingPostgresConfigError

    return ApiConfig(api_key)


@dataclass(frozen=True)
class Config:
    database: PostgresConfig
    api: ApiConfig


def load_settings() -> Config:
    database = load_postgres_config()
    api = load_api_config()

    return Config(
        database=database,
        api=api,
    )
