from dishka import Provider, Scope, WithParents, provide_all

from app.application.use_cases.create_initial_data import (
    CreateInitialDataUseCase,
)
from app.application.use_cases.get_organization_by_id import (
    GetOrganizationByIdUseCase,
)
from app.application.use_cases.get_organizations_by_building import (
    GetOrganizationsByBuildingUseCase,
)
from app.application.use_cases.search_organization_by_activity import (
    SearchOrganizationByActivityUseCase,
)
from app.application.use_cases.search_organization_by_name import (
    SearchOrganizationByNameUseCase,
)
from app.application.use_cases.search_organization_by_radius import (
    SearchOrganizationByRadiusUseCase,
)
from app.infrastructure.adapters.activity_gateway import SQLActivityGateway
from app.infrastructure.adapters.building_gateway import SQLBuildingGateway
from app.infrastructure.adapters.initial_gateway import SQLInitialDataGateway
from app.infrastructure.adapters.organization_gateway import (
    SQLOrganizationGateway,
)


class ApplicationProvider(Provider):
    gateways = provide_all(
        WithParents[SQLOrganizationGateway],
        WithParents[SQLBuildingGateway],
        WithParents[SQLActivityGateway],
        WithParents[SQLInitialDataGateway],
        scope=Scope.REQUEST,
    )

    use_cases = provide_all(
        SearchOrganizationByNameUseCase,
        GetOrganizationByIdUseCase,
        GetOrganizationsByBuildingUseCase,
        SearchOrganizationByRadiusUseCase,
        SearchOrganizationByActivityUseCase,
        CreateInitialDataUseCase,
        scope=Scope.REQUEST,
    )
