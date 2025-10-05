from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from app.application.use_cases.create_initial_data import (
    CreateInitialDataUseCase,
)

initial_data_router = APIRouter()


@initial_data_router.post(
    "/",
    summary="Create initial data",
    response_description="Result of initialization",
    responses={
        200: {"description": "Initial data created successfully"},
        401: {"description": "Missing API key"},
        403: {"description": "Invalid API key"},
        409: {"description": "Initial data already exists"},
    },
)
@inject
async def create_initial_data(
        use_case: FromDishka[CreateInitialDataUseCase],
) -> dict[str, str]:
    """
        Initializes the database with buildings, activities, and organizations.
    """
    await use_case()
    return {"result": "success"}
