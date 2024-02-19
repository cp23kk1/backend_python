from collections import defaultdict


class VocaverseResponse:
    status: dict[str, str]
    error: dict[str, str]
    data: dict[str, str]

    def __init__(
        self,
        status={"message": ""},
        error: dict[str, str] = {},
        data: dict[str, str] = {},
    ):
        self.status = status
        self.error = error
        self.data = data

    def dict(self):
        return {
            "status": self.status,
            "error": self.error,
            "data": self.data,
        }


class Error:
    status: dict[str, str]
    error: dict[str, str]

    def __init__(
        self,
        status={"message": "Failed"},
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
