from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

from app.application.common.models import Organization
from app.application.use_cases.get_organization_by_id import (
    GetOrganizationByIdUseCase,
)
from app.application.use_cases.search_organization_by_activity import (
    SearchOrganizationByActivityRequest,
    SearchOrganizationByActivityUseCase,
)
from app.application.use_cases.search_organization_by_name import (
    SearchOrganizationByNameRequest,
    SearchOrganizationByNameUseCase,
)
from app.application.use_cases.search_organization_by_radius import (
    SearchOrganizationByRadiusRequest,
    SearchOrganizationByRadiusUseCase,
)

organizations_router = APIRouter()

@organizations_router.get("/{organization_id}")
@inject
async def get_by_id(
        organization_id: int,
        use_case: FromDishka[GetOrganizationByIdUseCase],
) -> Organization:
    return await use_case(organization_id)

@organizations_router.get("/search/by-name")
@inject
async def search_by_name(
        use_case: FromDishka[SearchOrganizationByNameUseCase],
        data: Annotated[SearchOrganizationByNameRequest, Depends()],
) -> Organization:
    return await use_case(data)


@organizations_router.get("/search/by-radius")
@inject
async def search_by_radius(
        data: Annotated[SearchOrganizationByRadiusRequest, Depends()],
        use_case: FromDishka[SearchOrganizationByRadiusUseCase],
) -> list[Organization]:
    return await use_case(data)

@organizations_router.get("/search/by-activity")
@inject
async def search_by_activity(
        use_case: FromDishka[SearchOrganizationByActivityUseCase],
        data: Annotated[SearchOrganizationByActivityRequest, Depends()],
) -> list[Organization]:
    return await use_case(data)
