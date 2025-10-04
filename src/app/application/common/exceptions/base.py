from dataclasses import dataclass


@dataclass(eq=True)
class ApplicationError(Exception):

    @property
    def title(self) -> str:
        return "An application error occurred"
