from dataclasses import dataclass, field


@dataclass
class Building:
    id: int = field(init=False)
    address: str
    latitude: float
    longitude: float


@dataclass
class Activity:
    id: int = field(init=False)
    name: str
    parent_id: int | None = field(init=False)


@dataclass
class OrganizationPhone:
    id: int = field(init=False)
    organization_id: int = field(init=False)
    phone_number: str


@dataclass
class Organization:
    id: int = field(init=False)
    name: str
    building_id: int = field(init=False)
    is_active: bool
    building: Building
    activities: list[Activity] = field(default_factory=list)
    phones: list[OrganizationPhone] = field(default_factory=list)
