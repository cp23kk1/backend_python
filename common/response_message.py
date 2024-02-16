from dataclasses import dataclass
from typing import Dict, Optional
from http import HTTPStatus

@dataclass
class Response:
    status: str
    data: Dict[str, str]

@dataclass
class Error:
    status_code: HTTPStatus
    error: Dict[str, str]

@dataclass
class Result:
    def __init__(self, result, error: Optional[Error] = None):
        self.result = result
        self.error = error
