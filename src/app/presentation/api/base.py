from dataclasses import dataclass, field
from typing import TypeVar

TResult = TypeVar("TResult")
TError = TypeVar("TError")



@dataclass(frozen=True)
class Response:
    pass


@dataclass(frozen=True)
class ErrorData[TError]:
    title: str = "Unknown error occurred"
    data: TError | None = None


@dataclass(frozen=True)
class ErrorResponse[TError](Response):
    status: int = 500
    error: ErrorData[TError] = field(default_factory=ErrorData)
