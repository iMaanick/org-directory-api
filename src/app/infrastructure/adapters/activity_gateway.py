from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.common.models import Activity
from app.application.common.ports.activity_gateway import ActivityGateway
from app.infrastructure.sqlalchemy.mappings.activities import activities_table


class SQLActivityGateway(ActivityGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_name(
            self,
            name: str,
    ) -> Activity | None:
        stmt = (
            select(Activity)
            .where(func.lower(activities_table.c.name) == name.lower())
        )
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()
