from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.common.response import VocaverseResponse


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    error = {}
    error[exc.detail.__class__.__name__] = exc.detail.message
    return JSONResponse(
        content=VocaverseResponse(status={"message": "Failed"}, error=error).dict(),
        status_code=exc.status_code,
    )
