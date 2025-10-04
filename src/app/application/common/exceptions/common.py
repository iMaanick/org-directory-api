from app.application.common.exceptions.base import ApplicationError


class UnexpectedError(ApplicationError):
    pass


class NotFoundError(ApplicationError):
    def __init__(self, entity: str, field: str, value: str) -> None:
        self.entity = entity
        self.field = field
        self.value = value
        super().__init__()

    @property
    def title(self) -> str:
        return f"{self.entity} with {self.field}={self.value} not found"
