from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.application.common.models import OrganizationPhone
from app.infrastructure.sqlalchemy.registry import mapping_registry

organization_phones_table = Table(
    "organization_phones",
    mapping_registry.metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
    ),
    Column(
        "organization_id",
        Integer,
        ForeignKey("organizations.id"),
        nullable=False,
    ),
    Column(
        "phone_number",
        String(20),
        nullable=False,
    ),
)


def map_organization_phones_table() -> None:
    mapping_registry.map_imperatively(
        OrganizationPhone,
        organization_phones_table,
        properties={
            "organization": relationship(
                "Organization",
                back_populates="phones",
            ),
        },
    )
