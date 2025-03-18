"""Graceful shutdown module."""

from fastapi import Request, Response
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.pkg.logger import get_logger
from app.pkg.models.types.fastapi import FastAPITypes


class GracefulShutdownMiddleware(BaseHTTPMiddleware):
    """Graceful shutdown middleware class."""

    def __init__(self, fastapi_instance: FastAPITypes.instance, app: ASGIApp) -> None:
        """Init graceful shutdown middleware class."""

        super().__init__(app)
        self.fastapi_instance = fastapi_instance
        self.logger = get_logger(__name__)

    async def dispatch(self, request: Request, call_next) -> Response:
        """Dispatch request and check if fastapi state is not shutting down."""

        response: Response = await call_next(request)
        if self.fastapi_instance.state.shutting_down:
            return Response(
                "Service Unavailable",
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        return response
