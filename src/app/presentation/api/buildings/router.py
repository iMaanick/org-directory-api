from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from app.application.common.models import Organization
from app.application.use_cases.get_organizations_by_building import (
    GetOrganizationsByBuildingUseCase,
)

buildings_router = APIRouter()


@buildings_router.get("/{building_id}/organizations")
@inject
async def search_organizations_by_building_id(
        building_id: int,
        use_case: FromDishka[GetOrganizationsByBuildingUseCase],
) -> list[Organization]:
    return await use_case(building_id)
