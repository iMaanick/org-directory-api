from abc import abstractmethod
from typing import Protocol

from app.application.common.models import Activity


class ActivityGateway(Protocol):
    @abstractmethod
    async def get_by_name(
            self,
            name: str,
    ) -> Activity | None:
        raise NotImplementedError
