"""Module for testing read_by_country method of CityRepository."""

import pytest

from app.internal.repository.v1.postgresql import CityRepository
from app.pkg.models import v1 as models


@pytest.mark.postgresql
async def test_read_by_country(
    country_inserter,
    city_repository: CityRepository,
    city_inserter,
) -> None:
    result, _ = await country_inserter(country_code="RUS")

    city, city_cmd = await city_inserter(country_code=result.country_code)

    query = result.migrate(
        model=models.ReadCityByCountryQuery,
        extra_fields={"country_code": result.country_code},
    )

    cities = await city_repository.read_by_country(query=query)

    assert isinstance(cities, list)
    assert len(cities) == 1

    for response_city in cities:
        assert isinstance(response_city, models.City)
        assert response_city == city_cmd.migrate(
            model=models.City,
            extra_fields={"city_id": city.city_id},
        )


@pytest.mark.postgresql
async def test_read_by_country_empty(
    country_inserter,
    city_repository: CityRepository,
) -> None:
    result, _ = await country_inserter(country_code="RUS")

    query = result.migrate(
        model=models.ReadCityByCountryQuery,
        extra_fields={"country_id": result.country_id},
    )

    assert await city_repository.read_by_country(query=query) == []


@pytest.mark.postgresql
async def test_county_not_found(
    city_repository: CityRepository,
) -> None:
    query = models.ReadCityByCountryQuery.factory().build()

    assert await city_repository.read_by_country(query=query) == []
