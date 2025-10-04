import logging
from collections.abc import Callable
from functools import partial
from typing import Any

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request

from app.application.common.exceptions.auth import (
    InvalidApiKeyError,
    MissingApiKeyError,
)
from app.application.common.exceptions.base import ApplicationError
from app.application.common.exceptions.common import (
    InitialDataAlreadyExistsError,
    NotFoundError,
    UnexpectedError,
)
from app.presentation.api.base import ErrorData, ErrorResponse
from app.presentation.api.responses import ORJSONResponse

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        ApplicationError,
        error_handler(500),
    )
    app.add_exception_handler(
        UnexpectedError,
        error_handler(status.HTTP_502_BAD_GATEWAY),
    )
    app.add_exception_handler(
        NotFoundError,
        error_handler(status.HTTP_404_NOT_FOUND),
    )
    app.add_exception_handler(
        MissingApiKeyError,
        error_handler(status.HTTP_401_UNAUTHORIZED),
    )
    app.add_exception_handler(
        InvalidApiKeyError,
        error_handler(status.HTTP_403_FORBIDDEN),
    )
    app.add_exception_handler(
        InitialDataAlreadyExistsError,
        error_handler(status.HTTP_409_CONFLICT),
    )
    app.add_exception_handler(
        Exception,
        unknown_exception_handler,
    )


def error_handler(status_code: int) -> Callable[..., ORJSONResponse]:
    return partial(app_error_handler, status_code=status_code)


def app_error_handler(
        request: Request,
        err: ApplicationError,
        status_code: int,
) -> ORJSONResponse:
    return handle_error(
        request=request,
        err=err,
        err_data=ErrorData(title=err.title, data=err),
        status_code=status_code,
    )


def unknown_exception_handler(
        request: Request,
        err: Exception,
) -> ORJSONResponse:
    logger.exception("Unknown error occurred", exc_info=err)
    return ORJSONResponse(
        ErrorResponse(
            error=ErrorData(
                title=err.__class__.__name__,
                data={"message": str(err)},
            ),
        ),
        status_code=500,
    )


def handle_error(
        request: Request,
        err: Exception,
        err_data: ErrorData[Any],
        status_code: int,
) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResponse(error=err_data, status=status_code),
        status_code=status_code,
    )
