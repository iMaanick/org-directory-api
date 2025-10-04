from abc import abstractmethod
from typing import Protocol

from app.application.common.models import Building


class BuildingGateway(Protocol):
    @abstractmethod
    async def get_by_id(
            self,
            building_id: int,
    ) -> Building | None:
        raise NotImplementedError
