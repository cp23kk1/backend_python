from collections import defaultdict
from app.config.resource import Config

Config.load_config()


class VocaverseResponse:
    status: dict[str, str]
    data: dict[str, str]

    def __init__(
        self,
        status={"message": Config.SUCCESS},
        data: dict[str, str] = {},
    ):
        self.status = status
        self.data = data

    def dict(self):
        return {
            "status": self.status,
            "data": self.data,
        }


class Error:
    status: dict[str, str]
    error: dict[str, str]

    def __init__(
        self,
        status={"message": Config.FAILED},
        error: dict[str, str] = {},
    ):
        self.status = status
        self.error = error

    def dict(self):
        return {
            "status": self.status,
            "error": self.error,
        }


def convert_exception_to_error(exceptions: list) -> dict[str, str]:
    errors = defaultdict(list)
    for exception in exceptions:
        errors[exception.__class__.__name__].append(exception.__str__())
    return errors
