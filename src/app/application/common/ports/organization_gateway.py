from abc import abstractmethod
from typing import Protocol

from app.application.common.models import Organization


class OrganizationGateway(Protocol):
    @abstractmethod
    async def get_by_name(
            self,
            name: str,
    ) -> Organization | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
            self,
            organization_id: int,
    ) -> Organization | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_building_id(
            self,
            building_id: int,
    ) -> list[Organization]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_radius(
            self,
            center_lat: float,
            center_lng: float,
            radius_meters: float,
    ) -> list[Organization]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_activity(
            self,
            activity_name: str,
            max_depth: int = 3,
    ) -> list[Organization]:
        raise NotImplementedError
