from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from app.application.use_cases.create_initial_data import (
    CreateInitialDataUseCase,
)

initial_data_router = APIRouter()


@initial_data_router.post("/")
@inject
async def create_initial_data(
        use_case: FromDishka[CreateInitialDataUseCase],
) -> dict[str, str]:
    await use_case()
    return {"result": "success"}
