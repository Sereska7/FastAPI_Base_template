"""Service for manage cities."""

import typing

from app.internal.repository.v1.postgresql import city
from app.pkg.handlers.exception import handle_cancelled_error
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.city import CityNotFound, NoCityFoundForCountry
from app.pkg.models.v1.exceptions.repository import EmptyResult

__all__ = ["CityService"]


class CityService:
    """Service for manage cities."""

    city_repository: city.CityRepository

    def __init__(self):
        self.__logger = get_logger(__name__)

    @handle_cancelled_error
    async def create_city(self, cmd: models.CreateCityCommand) -> models.City:
        """Create city.

        Args:
            cmd: CreateCityCommand command.

        Returns:
            City: Created city.
        """
        self.__logger.debug("Creating city", extra={"cmd": cmd.to_dict()})
        return await self.city_repository.create(cmd=cmd)

    @handle_cancelled_error
    async def read_city(self, query: models.ReadCityQuery) -> models.City:
        """Read city.

        Args:
            query: ReadCityQuery query.

        Returns:
            City: Read city.
        """
        try:
            self.__logger.debug("Reading city", extra={"query": query.to_dict()})
            return await self.city_repository.read(query=query)
        except EmptyResult as e:
            raise CityNotFound from e

    @handle_cancelled_error
    async def read_cities_by_country(
        self,
        query: models.ReadCityByCountryQuery,
    ) -> typing.List[models.City]:
        """Read cities by country.

        Args:
            query: ReadCityByCountryQuery query.

        Returns:
            List[City]: Read cities by country.
        """
        try:
            self.__logger.debug(
                "Reading cities by country",
                extra={"query": query.to_dict()},
            )
            return await self.city_repository.read_by_country(query=query)
        except EmptyResult as e:
            raise NoCityFoundForCountry from e

    @handle_cancelled_error
    async def read_all_cities(self) -> typing.List[models.City]:
        """Read all cities.

        Returns:
            List[City]: Read all cities.
        """
        try:
            self.__logger.debug("Reading all cities")
            return await self.city_repository.read_all()
        except EmptyResult as e:
            raise CityNotFound from e

    @handle_cancelled_error
    async def update_city(self, cmd: models.UpdateCityCommand) -> models.City:
        """Update city.

        Args:
            cmd: UpdateCityCommand command.

        Returns:
            City: Updated city.
        """
        self.__logger.debug("Updating city", extra={"cmd": cmd.to_dict()})
        return await self.city_repository.update(cmd=cmd)

    @handle_cancelled_error
    async def delete_city(self, cmd: models.DeleteCityCommand) -> models.City:
        """Delete city.

        Args:
            cmd: DeleteCityCommand command.
        """
        self.__logger.debug("Deleting city", extra={"cmd": cmd.to_dict()})
        return await self.city_repository.delete(cmd=cmd)
