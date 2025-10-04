import logging
from dataclasses import dataclass

from app.application.common.exceptions.common import NotFoundError
from app.application.common.models import Organization
from app.application.common.ports.organization_gateway import (
    OrganizationGateway,
)
from app.infrastructure.auth.api_key_transport import ApiKeyTransport

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class SearchOrganizationByNameRequest:
    name: str


@dataclass(slots=True, frozen=True)
class SearchOrganizationByNameUseCase:
    organization_gateway: OrganizationGateway
    auth_key_manager: ApiKeyTransport

    async def __call__(
            self,
            request_data: SearchOrganizationByNameRequest,
    ) -> Organization:
        self.auth_key_manager.validate()
        organization = await self.organization_gateway.get_by_name(
            request_data.name,
        )
        if organization is None:
            raise NotFoundError(
                entity="organization",
                field="name",
                value=request_data.name,
            )
        return organization
