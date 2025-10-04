import logging
from dataclasses import dataclass

from app.application.common.exceptions.common import NotFoundError
from app.application.common.models import Organization
from app.application.common.ports.organization_gateway import (
    OrganizationGateway,
)
from app.infrastructure.auth.api_key_transport import ApiKeyTransport

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class GetOrganizationByIdUseCase:
    organization_gateway: OrganizationGateway
    auth_key_manager: ApiKeyTransport

    async def __call__(
            self,
            organization_id: int,
    ) -> Organization:
        self.auth_key_manager.validate()
        organization = await self.organization_gateway.get_by_id(
            organization_id,
        )
        if organization is None:
            raise NotFoundError(
                entity="organization",
                field="id",
                value=str(organization_id),
            )
        return organization
