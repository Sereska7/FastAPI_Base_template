"""Model City read_all method tests."""

import pytest

from app.internal.repository.v1.postgresql import CityRepository
from app.pkg.models import v1 as models


@pytest.mark.postgresql
@pytest.mark.slow
async def test_read_all(
    city_repository: CityRepository,
    city_inserter,
    country_inserter,
) -> None:

    result, _ = await country_inserter(country_code="RUS")
    city, city_cmd = await city_inserter(country_code=result.country_code)

    cities = await city_repository.read_all()

    assert isinstance(cities, list)
    assert len(cities) == 1

    for response_city in cities:
        assert isinstance(response_city, models.City)
        assert response_city == city_cmd.migrate(
            model=models.City,
            extra_fields={"city_id": city.city_id},
        )


@pytest.mark.postgresql
@pytest.mark.slow
async def test_read_all_empty(city_repository: CityRepository) -> None:

    assert await city_repository.read_all() == []
