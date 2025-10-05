from fastapi import APIRouter
from starlette.requests import Request

healthcheck_router = APIRouter()


@healthcheck_router.get(
    "/healthcheck",
    summary="Healthcheck endpoint",
    response_description="Status of the service",
)
async def healthcheck(_: Request) -> dict[str, str]:
    """
        Returns simple health status of the API.
    """
    return {"status": "ok"}
