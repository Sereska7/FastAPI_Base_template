"""Module with exceptions for Centrifugo."""

from starlette import status

from app.pkg.models.base import BaseAPIException
from app.pkg.models.types.strings import NotEmptyStr

__all__ = [
    "CentrifugoErrorResponse",
]


class CentrifugoErrorResponse(BaseAPIException):
    """Exception on centrifugo API error response.

    Attributes:
        status_code: int
            Status code of exception.
    """

    status_code = status.HTTP_200_OK

    def __init__(self, code: int, message: NotEmptyStr | str):
        """Init exception with Centrifugo API code and message.

        Args:
            code (int): Code from centrifugo API.
            message (NotEmptyStr | str): Response message from Centrifugo.
        """
        formatted_message = {"code": code, "message": message}
        super().__init__(formatted_message)
