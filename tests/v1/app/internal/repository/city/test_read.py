"""Module for testing read method of city repository."""

import pytest

from app.internal.repository.v1.postgresql import CityRepository
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_read(
    country_inserter,
    city_repository: CityRepository,
    city_inserter,
) -> None:
    result, _ = await country_inserter(country_code="RUS")

    city, city_cmd = await city_inserter(country_code=result.country_code)

    query = models.ReadCityQuery.factory().build(city_id=city.city_id)

    cities = await city_repository.read(query=query)

    assert isinstance(cities, models.City)
    assert cities == city_cmd.migrate(
        model=models.City,
        extra_fields={"city_id": city.city_id},
    )


@pytest.mark.postgresql
async def test_city_not_found(
    city_repository: CityRepository,
) -> None:
    query = models.ReadCityQuery.factory().build()

    with pytest.raises(EmptyResult):
        await city_repository.read(query=query)
