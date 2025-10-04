import logging
from dataclasses import dataclass

from app.application.common.exceptions.common import NotFoundError
from app.application.common.models import Organization
from app.application.common.ports.activity_gateway import ActivityGateway
from app.application.common.ports.organization_gateway import (
    OrganizationGateway,
)
from app.infrastructure.auth.api_key_transport import ApiKeyTransport

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class SearchOrganizationByActivityRequest:
    activity_name: str


@dataclass(slots=True, frozen=True)
class SearchOrganizationByActivityUseCase:
    organization_gateway: OrganizationGateway
    activity_gateway: ActivityGateway
    auth_key_manager: ApiKeyTransport

    async def __call__(
            self,
            request_data: SearchOrganizationByActivityRequest,
    ) -> list[Organization]:
        self.auth_key_manager.validate()
        activity = await self.activity_gateway.get_by_name(
            request_data.activity_name,
        )
        if activity is None:
            raise NotFoundError(
                entity="activity",
                field="name",
                value=request_data.activity_name,
            )
        return await self.organization_gateway.get_by_activity(
            request_data.activity_name,
        )
