from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from dishka.integrations.fastapi import setup_dishka
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import ORJSONResponse

from app.bootstrap.configs import load_settings
from app.bootstrap.ioc.containers import fastapi_container
from app.bootstrap.logger import setup_logging
from app.infrastructure.sqlalchemy.mappings.all import map_tables
from app.presentation.api.root import root_router
from app.presentation.exceptions import setup_exception_handlers


def init_routers(app: FastAPI) -> None:
    app.include_router(root_router)
    setup_exception_handlers(app)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    map_tables()
    yield
    await app.state.dishka_container.close()

def custom_openapi(app: FastAPI) ->  dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI",
        version="0.1.0",
        summary="",
        description="",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "APIKeyHeader": {
            "type": "apiKey",
            "name": "X-API-Key",
            "in": "header",
        },
    }

    openapi_schema["security"] = [{"APIKeyHeader": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def create_app() -> FastAPI:
    load_dotenv()
    setup_logging()
    app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
    init_routers(app)
    config = load_settings()
    container = fastapi_container(config)
    setup_dishka(container=container, app=app)
    app.openapi = lambda: custom_openapi(app)
    return app
