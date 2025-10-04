from fastapi import APIRouter

from app.presentation.api.buildings.router import buildings_router
from app.presentation.api.healthcheck.router import healthcheck_router
from app.presentation.api.initial_data.router import initial_data_router
from app.presentation.api.organizations.router import organizations_router

root_router = APIRouter()
root_router.include_router(healthcheck_router)
root_router.include_router(organizations_router, prefix="/organizations")
root_router.include_router(buildings_router, prefix="/buildings")
root_router.include_router(initial_data_router, prefix="/data_router")
