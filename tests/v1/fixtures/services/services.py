"""Fixtures for services."""

import pytest

from app.internal.repository.v1.postgresql import CityRepository, CountryRepository
from app.internal.services.v1 import CountryService
from app.internal.services.v1.city import CityService


@pytest.fixture()
async def city_service(city_repository: CityRepository) -> CityService:
    city_service_item = CityService()
    city_service_item.city_repository = city_repository
    return city_service_item


@pytest.fixture()
async def country_service(country_repository: CountryRepository) -> CountryService:
    country_service_item = CountryService()
    country_service_item.country_repository = country_repository
    return country_service_item
