"""All postgresql repositories are defined here."""

from dependency_injector import containers, providers

from app.internal.repository.v1.postgresql.city import CityRepository
from app.internal.repository.v1.postgresql.country import CountryRepository


class Repositories(containers.DeclarativeContainer):
    """Container for postgresql repositories."""

    city_repository = providers.Factory(CityRepository)
    country_repository = providers.Factory(CountryRepository)
