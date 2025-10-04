from abc import abstractmethod
from typing import Protocol


class ApiKeyTransport(Protocol):
    @abstractmethod
    def validate(self) -> None:
        raise NotImplementedError
