"""Repository for countries."""

from typing import List

from app.internal.repository.repository import Repository
from app.internal.repository.v1.postgresql.connection import get_connection
from app.internal.repository.v1.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.v1.postgresql.handlers.insert_changelog import (
    insert_changelog,
)
from app.pkg.models import v1 as models

__all__ = ["CountryRepository"]


class CountryRepository(Repository):
    """Country repository implementation."""

    @collect_response
    async def create(self, cmd: models.CreateCountryCommand) -> models.Country:
        """
        Create country.
        Args:
            cmd (models.CreateCountryCommand): CreateCountryCommand command.

        Returns:
            models.Country: Created country.
        """
        q = """
            insert into country (country_name, country_code)
            values (
                %(country_name)s,
                %(country_code)s
            )
            returning country_id, country_name, country_code
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadCountryQuery) -> models.Country:
        """
        Read country.
        Args:
            query (models.ReadCountryQuery): ReadCountryQuery query.

        Returns:
            models.Country: Read country.
        """
        q = """
            select
                country_id, country_name, country_code
            from country
            where country_id = %(country_id)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_all(self) -> List[models.Country]:
        """Read all countries.

        Returns:
            List[models.Country]: Read all countries.
        """
        q = """
            select
                country_id, country_name, country_code
            from country
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def update(self, cmd: models.UpdateCountryCommand) -> models.Country:
        """
        Update country.
        Args:
            cmd (models.UpdateCountryCommand): UpdateCountryCommand command.

        Returns:
            models.Country: Updated country.
        """
        q = """
            update country
            set
                country_name = %(country_name)s,
                country_code = %(country_code)s
            where country_id = %(country_id)s
            returning country_id, country_name, country_code
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeleteCountryCommand) -> models.Country:
        """
        Delete country.
        Args:
            cmd (models.DeleteCountryCommand): DeleteCountryCommand command.

        Returns:
            models.Country: Deleted country.
        """
        q = """
            delete from country
            where country_id = %(country_id)s
            returning country_id, country_name, country_code
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
