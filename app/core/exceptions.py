from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


class AppException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class ConflictException(AppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message=message, status_code=status.HTTP_409_CONFLICT)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )
    logger.exception(f"Unhandled exception on {request.method} {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )
