import logging
from dataclasses import dataclass

from app.application.common.exceptions.common import NotFoundError
from app.application.common.models import Organization
from app.application.common.ports.building_gateway import BuildingGateway
from app.application.common.ports.organization_gateway import (
    OrganizationGateway,
)
from app.infrastructure.auth.api_key_transport import ApiKeyTransport

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class GetOrganizationsByBuildingUseCase:
    organization_gateway: OrganizationGateway
    building_gateway: BuildingGateway
    auth_key_manager: ApiKeyTransport

    async def __call__(
            self,
            building_id: int,
    ) -> list[Organization]:
        self.auth_key_manager.validate()
        building = await self.building_gateway.get_by_id(building_id)
        if building is None:
            raise NotFoundError(
                entity="building",
                field="id",
                value=str(building_id),
            )
        return await self.organization_gateway.get_by_building_id(
            building_id,
        )
