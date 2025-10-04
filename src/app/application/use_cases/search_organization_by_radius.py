import logging
from dataclasses import dataclass

from app.application.common.models import Organization
from app.application.common.ports.organization_gateway import (
    OrganizationGateway,
)
from app.infrastructure.auth.api_key_transport import ApiKeyTransport

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class SearchOrganizationByRadiusRequest:
    center_lat: float
    center_lng: float
    radius: float


@dataclass(slots=True, frozen=True)
class SearchOrganizationByRadiusUseCase:
    organization_gateway: OrganizationGateway
    auth_key_manager: ApiKeyTransport

    async def __call__(
            self,
            request_data: SearchOrganizationByRadiusRequest,
    ) -> list[Organization]:
        self.auth_key_manager.validate()
        return await self.organization_gateway.get_by_radius(
            center_lat=request_data.center_lat,
            center_lng=request_data.center_lng,
            radius_meters=request_data.radius,
        )
