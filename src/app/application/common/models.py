from dataclasses import dataclass, field


@dataclass
class Building:
    address: str
    latitude: float
    longitude: float
    id: int | None = None


@dataclass
class Activity:
    name: str
    id: int | None = None
    parent_id: int | None = None


@dataclass
class OrganizationPhone:
    organization_id: int = field(init=False)
    phone_number: str
    id: int | None = None


@dataclass
class Organization:
    name: str
    is_active: bool
    building: Building
    activities: list[Activity] = field(default_factory=list)
    phones: list[OrganizationPhone] = field(default_factory=list)
    id: int | None = None
    building_id: int | None = None
