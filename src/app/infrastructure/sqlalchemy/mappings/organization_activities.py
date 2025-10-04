from sqlalchemy import Column, ForeignKey, Integer, Table

from app.infrastructure.sqlalchemy.registry import mapping_registry

organization_activities_table = Table(
    "organization_activities",
    mapping_registry.metadata,
    Column(
        "organization_id",
        Integer,
        ForeignKey("organizations.id"),
        primary_key=True,
    ),
    Column(
        "activity_id",
        Integer,
        ForeignKey("activities.id"),
        primary_key=True,
    ),
)
