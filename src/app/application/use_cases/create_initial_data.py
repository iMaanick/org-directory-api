import logging
from dataclasses import dataclass

from app.application.common.ports.initial_gateway import InitialDataGateway
from app.infrastructure.auth.api_key_transport import ApiKeyTransport

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class CreateInitialDataUseCase:
    initial_data_gateway: InitialDataGateway
    auth_key_manager: ApiKeyTransport

    async def __call__(
            self,
    ) -> None:
        self.auth_key_manager.validate()
        await self.initial_data_gateway.create_initial_data()
