from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from app.application.common.models import Organization
from app.application.use_cases.get_organizations_by_building import (
    GetOrganizationsByBuildingUseCase,
)

buildings_router = APIRouter()


@buildings_router.get(
    "/{building_id}/organizations",
    summary="Get organizations by building ID",
    response_description="List of organizations in the specified building",
    responses={
        200: {"description": "Organizations found"},
        401: {"description": "Missing API key"},
        403: {"description": "Invalid API key"},
        404: {"description": "Building not found"},
    },
)
@inject
async def search_organizations_by_building_id(
        building_id: int,
        use_case: FromDishka[GetOrganizationsByBuildingUseCase],
) -> list[Organization]:
    """
    Returns all organizations located in the specified building.

    Parameters:
    - **building_id**: The ID of the building to search organizations in.
    """
    return await use_case(building_id)
