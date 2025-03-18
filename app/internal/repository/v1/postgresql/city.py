"""Repository for cities."""

from typing import List

from app.internal.repository.repository import Repository
from app.internal.repository.v1.postgresql.connection import get_connection
from app.internal.repository.v1.postgresql.handlers.collect_response import (
    collect_response,
)
from app.pkg.models import v1 as models

__all__ = ["CityRepository"]


class CityRepository(Repository):
    """City repository implementation."""

    @collect_response
    async def create(self, cmd: models.CreateCityCommand) -> models.City:
        """
        Create city.
        Args:
            cmd (models.CreateCityCommand): CreateCityCommand command.

        Returns:
            models.City: Created city.
        """
        q = """
            insert into city (city_name, city_code, country_id)
            values (
                %(city_name)s,
                %(city_code)s,
                (select country_id from country where country_code = %(country_code)s)
            )
            returning
                city_id,
                city_name,
                city_code,
                (select country_code from country where city.country_id = country.country_id);
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadCityQuery) -> models.City:
        """
        Read city.
        Args:
            query (models.ReadCityQuery): ReadCityQuery query.

        Returns:
            models.City: Read city.
        """
        q = """
            select city_id,
                   city_name,
                   city_code,
                   country_code
            from city
                     join country c on c.country_id = city.country_id
            where city_id = %(city_id)s;
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_by_country(
        self,
        query: models.ReadCityByCountryQuery,
    ) -> List[models.City]:
        """
        Read cities by country.
        Args:
            query (models.ReadCityByCountryQuery): ReadCityByCountryQuery query.

        Returns:
            List[models.City]: Read cities by country.
        """
        q = """
            select city_id,
                   city_name,
                   city_code,
                   country_code
            from city
                     join country c on c.country_id = city.country_id
            where country_code = %(country_code)s;
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchall()

    @collect_response
    async def read_all(self) -> List[models.City]:
        q = """
            select city_id,
                   city_name,
                   city_code,
                   country_code
            from city
                     join country on country.country_id = city.country_id;
        """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def update(self, cmd: models.UpdateCityCommand) -> models.City:
        """
        Update city.
        Args:
            cmd (models.UpdateCityCommand): UpdateCityCommand command.

        Returns:
            models.City: Updated city
        """
        q = """
            update city
            set city_name  = coalesce(%(city_name)s, city_name),
                city_code  = coalesce(%(city_code)s, city_code),
                country_id = coalesce((select country_id from country where country_code = %(country_code)s), country_id)
            where city_id = %(city_id)s
            returning
                city_id,
                city_name,
                city_code,
                (select country_code from country where city.country_id = country.country_id);
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeleteCityCommand) -> models.City:
        """
        Delete city.
        Args:
            cmd (models.DeleteCityCommand): DeleteCityCommand command.

        Returns:
            models.City: Deleted city
        """
        q = """
            delete
            from city
            where city_id = %(city_id)s
            returning
                city_id,
                city_name,
                city_code,
                (select country_code from country where city.country_id = country.country_id);
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
