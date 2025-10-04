from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.application.common.models import Organization
from app.infrastructure.sqlalchemy.mappings.organization_activities import (
    organization_activities_table,
)
from app.infrastructure.sqlalchemy.registry import mapping_registry

organizations_table = Table(
    "organizations",
    mapping_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255), nullable=False, unique=True),
    Column("building_id", Integer, ForeignKey("buildings.id"), nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
)


def map_organizations_table() -> None:
    mapping_registry.map_imperatively(
        Organization,
        organizations_table,
        properties={
            "building": relationship(
                "Building",
                back_populates="organizations",
                lazy="selectin",
            ),
            "activities": relationship(
                "Activity",
                secondary=organization_activities_table,
                back_populates="organizations",
                lazy="selectin",
            ),
            "phones": relationship(
                "OrganizationPhone",
                back_populates="organization",
                lazy="selectin",
            ),
        },
    )
