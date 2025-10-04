from app.application.common.exceptions.base import ApplicationError


class MissingApiKeyError(ApplicationError):
    def __init__(self, header_name: str) -> None:
        self.header_name = header_name
        super().__init__()

    @property
    def title(self) -> str:
        return f"API key is missing in header '{self.header_name}'"


class InvalidApiKeyError(ApplicationError):
    def __init__(self, header_name: str, provided_value: str) -> None:
        self.header_name = header_name
        self.provided_value = provided_value
        super().__init__()

    @property
    def title(self) -> str:
        return (
            f"Invalid API key '{self.provided_value}' "
            f"in header '{self.header_name}'"
        )
