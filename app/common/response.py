from dataclasses import dataclass
from typing import Dict, List, Optional
from http import HTTPStatus


@dataclass
class Response:
    status: str
    error: Dict[str, str]
    data: List

    def __init__(
        self, status: str = "", error: Optional[Dict[str, str]] = None, data=None
    ):
        self.status = status
        self.error = error if error is not None else {}
        self.data = data if data is not None else []


@dataclass
class Error:
    status_code: HTTPStatus
    message: str


# @dataclass
# class Result:
#     def __init__(self, result, error: Optional[Dict[str, str]] = None):
#         self.result = result
#         self.error = error
