from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.common.response import Error


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    error = {}
    error['message'] = exc.detail.message
    return JSONResponse(
        content=Error(error=error).dict(),
        status_code=exc.status_code,
    )
