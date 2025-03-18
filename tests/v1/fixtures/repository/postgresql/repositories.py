"""All fixtures for postgresql repositories."""

import pytest

from app.internal.repository.v1.postgresql import CityRepository, CountryRepository


@pytest.fixture()
async def city_repository() -> CityRepository:
    return CityRepository()


@pytest.fixture()
async def country_repository() -> CountryRepository:
    return CountryRepository()
