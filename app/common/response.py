from collections import defaultdict


class Status:
    status: str
    message: dict[str, str]

    def __init__(self, status: str = "", message: dict[str, str] = None):
        self.status = status
        self.message = message if message is not None else {}


class Response:
    status: Status
    data: list | str

    def __init__(self, status: Status, data=None):
        self.status = status
        self.data = [] if data is None else data


class Result:
    value: any
    err: list

    def __init__(self, value: any, err=None):
        self.value = value
        self.err = [] if err is None else err


def convert_exception_to_error(exceptions: list) -> dict[str, str]:
    errors = defaultdict(list)
    for exception in exceptions:
        errors[exception.__class__.__name__].append(exception.__str__())
    return errors
