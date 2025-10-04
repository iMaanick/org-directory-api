from sqlalchemy.ext.asyncio import AsyncSession

from app.application.common.models import Building, Activity, Organization, OrganizationPhone
from app.application.common.ports.initial_gateway import InitialDataGateway


class SQLInitialDataGateway(InitialDataGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_initial_data(self) -> None:
        # I was too lazy to do it properly, so this came out, please understand and forgive me =)

        buildings = [
            Building(address="г. Москва, ул. Ленина 1, офис 3", latitude=55.7558, longitude=37.6173),
            Building(address="г. Новосибирск, ул. Блюхера 32/1", latitude=55.0302, longitude=82.9204),
        ]

        food = Activity(name="Еда")
        cars = Activity(name="Автомобили")

        meat = Activity(name="Мясная продукция")
        meat.parent = food
        milk = Activity(name="Молочная продукция")
        milk.parent = food

        truck = Activity(name="Грузовые")
        truck.parent = cars
        car = Activity(name="Легковые")
        car.parent = cars

        parts = Activity(name="Запчасти")
        parts.parent = car
        accessories = Activity(name="Аксессуары")
        accessories.parent = car

        activities = [food, meat, milk, cars, truck, car, parts, accessories]

        organizations = [
            Organization(
                name="ООО Рога и Копыта",
                building=buildings[1],
                is_active=True,
                phones=[
                    OrganizationPhone(phone_number="2-222-222"),
                    OrganizationPhone(phone_number="3-333-333"),
                    OrganizationPhone(phone_number="8-923-666-13-13"),
                ],
            ),
            Organization(
                name="ЗАО Мясокомбинат Сибирский",
                building=buildings[0],
                is_active=True,
                phones=[
                    OrganizationPhone(phone_number="+7-495-111-22-33"),
                ],
            ),
            Organization(
                name="ИП Иванов Автосервис",
                building=buildings[0],
                is_active=True,
                phones=[
                    OrganizationPhone(phone_number="+7-495-222-33-44"),
                ],
            ),
        ]

        organizations[0].activities.extend([activities[1], activities[2]])
        organizations[1].activities.append(activities[1])
        organizations[2].activities.extend([activities[5], activities[6]])

        self.session.add_all(buildings + activities + organizations)
