import logging
from dataclasses import dataclass

from app.application.common.exceptions.common import InitialDataAlreadyExistsError
from app.application.common.ports.initial_gateway import InitialDataGateway
from app.application.common.ports.organization_gateway import OrganizationGateway
from app.application.common.ports.uow import UoW
from app.infrastructure.auth.api_key_transport import ApiKeyTransport

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class CreateInitialDataUseCase:
    initial_data_gateway: InitialDataGateway
    organization_gateway: OrganizationGateway
    auth_key_manager: ApiKeyTransport
    uow: UoW

    async def __call__(
            self,
    ) -> None:
        self.auth_key_manager.validate()
        organization = await self.organization_gateway.get_by_id(1)
        if organization:
            raise InitialDataAlreadyExistsError()
        await self.initial_data_gateway.create_initial_data()
        await self.uow.commit()
