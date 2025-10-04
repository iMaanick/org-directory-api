from app.infrastructure.sqlalchemy.mappings.activities import (
    map_activities_table,
)
from app.infrastructure.sqlalchemy.mappings.buildings import (
    map_buildings_table,
)
from app.infrastructure.sqlalchemy.mappings.organization_phones import (
    map_organization_phones_table,
)
from app.infrastructure.sqlalchemy.mappings.organizations import (
    map_organizations_table,
)


def map_tables() -> None:
    map_activities_table()
    map_buildings_table()
    map_organization_phones_table()
    map_organizations_table()
