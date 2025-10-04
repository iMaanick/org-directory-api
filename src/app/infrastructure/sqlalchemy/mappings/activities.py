from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.application.common.models import Activity
from app.infrastructure.sqlalchemy.mappings.organization_activities import (
    organization_activities_table,
)
from app.infrastructure.sqlalchemy.registry import mapping_registry

activities_table = Table(
    "activities",
    mapping_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("parent_id", Integer, ForeignKey("activities.id"), nullable=True),
)


def map_activities_table() -> None:
    mapping_registry.map_imperatively(
        Activity,
        activities_table,
        properties={
            "parent": relationship(
                "Activity",
                remote_side=[activities_table.c.id],
            ),
            "organizations": relationship(
                "Organization",
                secondary=organization_activities_table,
                back_populates="activities",
            ),
        },

    )
