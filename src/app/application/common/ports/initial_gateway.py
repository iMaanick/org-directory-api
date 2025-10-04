from abc import abstractmethod
from typing import Protocol


class InitialDataGateway(Protocol):
    @abstractmethod
    async def create_initial_data(self) -> None:
        raise NotImplementedError
