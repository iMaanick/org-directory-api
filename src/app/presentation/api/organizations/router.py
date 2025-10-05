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


@organizations_router.get(
    "/{organization_id}",
    summary="Get organization by ID",
    response_description="Organization details",
    responses={
        200: {"description": "Organization found"},
        401: {"description": "Missing API key"},
        403: {"description": "Invalid API key"},
        404: {"description": "Organization not found"},
    },
)
@inject
async def get_by_id(
        organization_id: int,
        use_case: FromDishka[GetOrganizationByIdUseCase],
) -> Organization:
    """
    Returns the organization with the specified ID.

    Parameters:
    - **organization_id**: The ID of the organization to retrieve.
    """
    return await use_case(organization_id)


@organizations_router.get(
    "/search/by-name",
    summary="Search organization by name",
    response_description="Organization details",
    responses={
        200: {"description": "Organization found"},
        401: {"description": "Missing API key"},
        403: {"description": "Invalid API key"},
        404: {"description": "Organization not found"},
    },
)
@inject
async def search_by_name(
        use_case: FromDishka[SearchOrganizationByNameUseCase],
        data: Annotated[SearchOrganizationByNameRequest, Depends()],
) -> Organization:
    """
    Searches for an organization by its name.

    Parameters:
    - **name**: Name of the organization to search for.
    """
    return await use_case(data)


@organizations_router.get(
    "/search/by-radius",
    summary="Search organizations within radius",
    response_description=(
            "List of organizations found within the specified radius"
    ),
    responses={
        200: {"description": "Organizations found"},
        401: {"description": "Missing API key"},
        403: {"description": "Invalid API key"},
    },
)
@inject
async def search_by_radius(
        data: Annotated[SearchOrganizationByRadiusRequest, Depends()],
        use_case: FromDishka[SearchOrganizationByRadiusUseCase],
) -> list[Organization]:
    """
    Searches for organizations within a given radius
    from the specified coordinates.
    Parameters:
    - **center_lat**: Latitude of the center point.
    - **center_lng**: Longitude of the center point.
    - **radius**: Search radius in meters.
    """
    return await use_case(data)


@organizations_router.get(
    "/search/by-activity",
    summary="Search organizations by activity",
    response_description=(
            "List of organizations associated with the specified activity"
    ),
    responses={
        200: {"description": "Organizations found"},
        401: {"description": "Missing API key"},
        403: {"description": "Invalid API key"},
        404: {"description": "Activity not found"},
    },
)
@inject
async def search_by_activity(
        use_case: FromDishka[SearchOrganizationByActivityUseCase],
        data: Annotated[SearchOrganizationByActivityRequest, Depends()],
) -> list[Organization]:
    """
    Searches for organizations linked to a given activity name.

    Parameters:
    - **activity_name**: Name of the activity to filter organizations by.
    """
    return await use_case(data)
