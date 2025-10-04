from sqlalchemy import Column, Float, Integer, String, Table
from sqlalchemy.orm import relationship

from app.application.common.models import Building
from app.infrastructure.sqlalchemy.registry import mapping_registry

buildings_table = Table(
    "buildings",
    mapping_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("address", String(255), nullable=False),
    Column("latitude", Float, nullable=False),
    Column("longitude", Float, nullable=False),
)


def map_buildings_table() -> None:
    mapping_registry.map_imperatively(
        Building,
        buildings_table,
        properties={
            "organizations": relationship(
                "Organization",
                back_populates="building",
            ),
        },
    )
