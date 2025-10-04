from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.common.models import Building
from app.application.common.ports.building_gateway import BuildingGateway
from app.infrastructure.sqlalchemy.mappings.buildings import buildings_table


class SQLBuildingGateway(BuildingGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(
            self,
            building_id: int,
    ) -> Building | None:
        stmt = (
            select(Building)
            .where(buildings_table.c.id == building_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()
