"""Models for country object."""

import typing

from app.internal.repository.v1.postgresql import country
from app.internal.services.v1.city import CityService
from app.pkg.handlers.exception import handle_cancelled_error
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.country import (
    CountryNameAlreadyExists,
    CountryNotFound,
)
from app.pkg.models.v1.exceptions.repository import EmptyResult, UniqueViolation

__all__ = ["CountryService"]


class CountryService:
    """Service for manage countries."""

    country_repository: country.CountryRepository
    city_service: CityService

    def __init__(self):
        self.__logger = get_logger(__name__)

    @handle_cancelled_error
    async def create_country(self, cmd: models.CreateCountryCommand) -> models.Country:
        """Create country.

        Args:
            cmd: CreateCountryCommand command.

        Returns:
            Country: Created country.
        """
        try:
            self.__logger.debug("Creating country", extra={"cmd": cmd.to_dict()})
            return await self.country_repository.create(cmd=cmd)
        except UniqueViolation as e:
            raise CountryNameAlreadyExists from e

    @handle_cancelled_error
    async def read_country(self, query: models.ReadCountryQuery) -> models.Country:
        """Read country.

        Args:
            query: ReadCountryQuery query.

        Returns:
            Country: Read country.
        """
        self.__logger.debug("Reading country", extra={"query": query.to_dict()})
        return await self.country_repository.read(query=query)

    @handle_cancelled_error
    async def read_all_countries(self) -> typing.List[models.Country]:
        """Read all countries.

        Returns:
            List[Country]: Read all countries.
        """
        self.__logger.debug("Reading all countries")
        return await self.country_repository.read_all()

    @handle_cancelled_error
    async def update_country(self, cmd: models.UpdateCountryCommand) -> models.Country:
        """Update country.

        Args:
            cmd: UpdateCountryCommand command.

        Returns:
            Country: Updated country.
        """
        try:
            self.__logger.debug("Updating country", extra={"cmd": cmd.to_dict()})
            return await self.country_repository.update(cmd=cmd)
        except EmptyResult as e:
            raise CountryNotFound from e

    @handle_cancelled_error
    async def delete_country(self, cmd: models.DeleteCountryCommand) -> models.Country:
        """Delete country.

        Args:
            cmd: DeleteCountryCommand command.
        """
        self.__logger.debug("Deleting country", extra={"cmd": cmd.to_dict()})
        return await self.country_repository.delete(cmd=cmd)

    @handle_cancelled_error
    async def read_country_with_cities(self) -> typing.List[models.CountryWithCities]:
        """Read country with cities.

        Note:
            This method is used as an example of injecting one service into another.

        Returns:
            typing.List[models.CountryWithCities]: Read countries with cities.
        """
        result = []
        self.__logger.debug("Reading countries with cities")
        for country_item in await self.country_repository.read_all():
            cities = await self.city_service.read_cities_by_country(
                query=models.ReadCityByCountryQuery(
                    country_code=country_item.country_code,
                ),
            )
            result.append(
                country_item.migrate(
                    models.CountryWithCities,
                    extra_fields={"cities": cities},
                ),
            )
        return result
