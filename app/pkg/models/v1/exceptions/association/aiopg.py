"""Here you can pass the postgres error codes with association python
exceptions."""

from psycopg2 import errorcodes

from app.pkg.models.v1.exceptions import city, country, repository

__all__ = ["__aiopg__", "__constrains__"]


__aiopg__ = {
    errorcodes.UNIQUE_VIOLATION: repository.UniqueViolation,
}

# TODO: Make this dict more flexible.
#       Like `Container` class in `/app/pkg/models/core/container.py`
#       Add support for owerwrite exceptions in `__aiopg__` dict.
__constrains__ = {
    **city.__constrains__,
    **country.__constrains__,
}
