from sqlalchemy import Integer, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.application.common.models import (
    Organization,
)
from app.application.common.ports.organization_gateway import (
    OrganizationGateway,
)
from app.infrastructure.sqlalchemy.mappings.activities import activities_table
from app.infrastructure.sqlalchemy.mappings.buildings import buildings_table
from app.infrastructure.sqlalchemy.mappings.organization_activities import (
    organization_activities_table,
)
from app.infrastructure.sqlalchemy.mappings.organizations import (
    organizations_table,
)


class SQLOrganizationGateway(OrganizationGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_name(
            self,
            name: str,
    ) -> Organization | None:
        stmt = (
            select(Organization)
            .where(func.lower(organizations_table.c.name) == name.lower())
        )
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def get_by_id(
            self,
            organization_id: int,
    ) -> Organization | None:
        stmt = (
            select(Organization)
            .where(organizations_table.c.id == organization_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def get_by_building_id(
            self,
            building_id: int,
    ) -> list[Organization]:
        stmt = (
            select(Organization)
            .where(organizations_table.c.building_id == building_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_radius(
            self,
            center_lat: float,
            center_lng: float,
            radius_meters: float,
    ) -> list[Organization]:
        """
        Get all organizations located in buildings within radius_meters of the point (center_lat, center_lng)
        """
        earth_radius = 6371000  # Earth's radius in meters

        stmt = (
            select(Organization)
            .join(buildings_table, organizations_table.c.building_id == buildings_table.c.id)
            .where(
                (
                        earth_radius * func.acos(
                    func.cos(func.radians(center_lat))
                    * func.cos(func.radians(buildings_table.c.latitude))
                    * func.cos(func.radians(buildings_table.c.longitude) - func.radians(center_lng))
                    + func.sin(func.radians(center_lat))
                    * func.sin(func.radians(buildings_table.c.latitude)),
                )
                ) <= radius_meters,
            )
        )

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_activity(
            self,
            activity_name: str,
            max_depth: int = 3,
    ) -> list[Organization]:
        """
        Получить все организации, которые относятся к указанному виду деятельности
        включая все подвиды до 3 уровня.
        """
        # начальный уровень (root activity)
        cte = (
            select(activities_table.c.id, activities_table.c.parent_id, func.cast(1, Integer).label("level"))
            .where(func.lower(activities_table.c.name) == activity_name.lower())
            .cte(name="activity_tree", recursive=True)
        )

        activity_alias = aliased(activities_table)

        # рекурсивное подключение потомков
        cte = cte.union_all(
            select(
                activity_alias.c.id,
                activity_alias.c.parent_id,
                (cte.c.level + 1).label("level"),
            ).where(
                activity_alias.c.parent_id == cte.c.id,
            ).where(
                (cte.c.level + 1) <= max_depth,
            ),
        )

        # присоединяем организации через связующую таблицу
        stmt = (
            select(Organization)
            .join(organization_activities_table, Organization.id == organization_activities_table.c.organization_id)
            .join(cte, organization_activities_table.c.activity_id == cte.c.id)
            .distinct()
        )

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
