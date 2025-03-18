"""Handle Postgresql Query Exceptions."""

from typing import Any, Callable, Coroutine

import psycopg2

from app.pkg.logger import get_logger
from app.pkg.models.base import Model
from app.pkg.models.v1.exceptions.association import __aiopg__, __constrains__
from app.pkg.models.v1.exceptions.repository import DriverError

__all__ = ["handle_exception"]

logger = get_logger(__name__)


def handle_exception(func: Callable[..., Model]) -> Callable[
    [tuple[object, ...], dict[str, object]],
    Coroutine[Any, Any, Model],
]:
    """Decorator Catching Postgresql Query Exceptions.

    Args:
        func:
            callable function object.

    Examples:
        If you have a function that contains a query in postgresql,
        decorator :func:`.handle_exception` will catch the exceptions that can be
        raised by the query::

            >>> from app.pkg.models import v1 as models
            >>> from app.internal.repository.postgresql.connection import get_connection
            >>> @handle_exception
            ... async def create(self, cmd: models.CreateUserRoleCommand) -> None:
            ...     q = \"""
            ...         insert into user_roles(role_name) values (%(role_name)s)
            ...         on conflict do nothing returning role_name;
            ...     \"""
            ...     async with get_connection() as cur:
            ...         await cur.execute(q, cmd.to_dict(show_secrets=True))

    Returns:
        Result of call function.

    Raises:
        UniqueViolation: The query violates the domain uniqueness constraints
            of the database set.
        DriverError: Any error during execution query on a database.
    """

    async def wrapper(*args: object, **kwargs: object) -> Model:
        """Inner function. Catching Postgresql Query Exceptions.

        Args:
            *args:
                Positional arguments.
            **kwargs:
                Keyword arguments.

        Raises:
            UniqueViolation: The query violates the domain uniqueness constraints
                of the database set.
            DriverError: Any error during execution query on an database.

        Returns:
            Result of call function.
        """

        try:
            return await func(*args, **kwargs)
        except psycopg2.Error as error:
            if exc := __constrains__.get(error.diag.constraint_name):
                logger.exception(error.diag.message_detail)
                raise exc from error

            if exc := __aiopg__.get(error.pgcode):
                logger.exception(error.diag.message_detail)
                raise exc from error

            logger.exception("Something went wrong with sql query.")
            raise DriverError(error_details=error.pgerror) from error

    return wrapper
