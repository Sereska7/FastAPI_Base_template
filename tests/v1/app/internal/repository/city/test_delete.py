"""Module for testing update method of country repository."""

import pytest

from app.internal.repository.v1.postgresql import CityRepository
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.repository import EmptyResult


@pytest.mark.postgresql
@pytest.mark.slow
async def test_delete(
    city_repository: CityRepository,
    country_inserter,
    city_inserter,
) -> None:

    result, _ = await country_inserter(country_code="RUS")

    city, _ = await city_inserter(country_code=result.country_code)

    cmd = city.migrate(
        models.DeleteCityCommand,
        extra_fields={"id": city.city_id},
    )

    await city_repository.delete(cmd=cmd)

    with pytest.raises(EmptyResult):
        await city_repository.read(
            query=city.migrate(models.ReadCityQuery, extra_fields={"id": city.city_id}),
        )


@pytest.mark.postgresql
async def test_city_not_found(
    city_repository: CityRepository,
    # create_model,
) -> None:
    cmd = models.DeleteCityCommand.factory().build()

    with pytest.raises(EmptyResult):
        await city_repository.delete(cmd=cmd)
