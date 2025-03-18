"""Country and city inserters for PostgreSQL repository."""

import pytest

from app.internal.repository.v1.postgresql import CityRepository, CountryRepository
from app.pkg.models import v1 as models
from tests.fixtures.repository.postgresql.inserters import __inserter


@pytest.fixture()
async def country_inserter(
    country_repository: CountryRepository,
) -> callable:
    """Insert country to database."""

    return lambda **kwargs: __inserter(
        repository=country_repository,
        cmd_model=models.CreateCountryCommand,
        **kwargs,
    )


@pytest.fixture()
async def city_inserter(
    city_repository: CityRepository,
) -> callable:
    """Insert city to database."""

    return lambda **kwargs: __inserter(
        repository=city_repository,
        cmd_model=models.CreateCityCommand,
        **kwargs,
    )
