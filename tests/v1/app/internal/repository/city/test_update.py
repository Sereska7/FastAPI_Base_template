"""Module for testing city repository update method."""

import asyncio

import pytest

from app.internal.repository.v1.postgresql import CityRepository
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.city import CityNameAlreadyExists, DuplicateCityCode
from app.pkg.models.v1.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_update(
    city_repository: CityRepository,
    city_inserter,
    country_inserter,
) -> None:
    country, _ = await country_inserter(country_code="RUS")
    city, _ = await city_inserter(country_code=country.country_code)

    cmd = city.migrate(
        models.UpdateCityCommand,
        extra_fields={"city_name": "Moscow", "city_code": "MSK"},
    )

    await city_repository.update(cmd=cmd)

    result = await city_repository.read(
        query=city.migrate(
            models.ReadCityQuery,
            extra_fields={"city_id": city.city_id},
        ),
    )

    assert result == cmd.migrate(
        model=models.City,
        extra_fields={"city_id": city.city_id},
    )


@pytest.mark.postgresql
async def test_city_not_found(
    city_repository: CityRepository,
    country_inserter,
    city_inserter,
) -> None:
    result, _ = await country_inserter()
    city, _ = await city_inserter(country_code=result.country_code)
    cmd = models.UpdateCityCommand.factory().build(
        city_id=city.city_id + 1,
        city_name=city.city_name + "a",
    )

    with pytest.raises(EmptyResult):
        await city_repository.update(cmd=cmd)


@pytest.mark.postgresql
async def test_duplicate_city_code(
    city_repository: CityRepository,
    country_inserter,
) -> None:

    result, _ = await country_inserter()
    cmd_1 = models.CreateCityCommand.factory().build(
        country_code=result.country_code,
        city_code="MSK",
        city_name="Ufa",
    )
    cmd_2 = models.CreateCityCommand.factory().build(
        country_code=result.country_code,
        city_code="MSK",
        city_name="Moscow",
    )

    tasks = [
        asyncio.create_task(city_repository.create(cmd=cmd_1)),
        asyncio.create_task(city_repository.create(cmd=cmd_2)),
    ]

    with pytest.raises(DuplicateCityCode):
        await asyncio.gather(*tasks)


@pytest.mark.postgresql
async def test_duplicate_city_name(
    city_repository: CityRepository,
    country_inserter,
) -> None:

    result, _ = await country_inserter()

    cmd_1 = models.CreateCityCommand.factory().build(
        country_code=result.country_code,
        city_code="UFA",
        city_name="Moscow",
    )
    cmd_2 = models.CreateCityCommand.factory().build(
        country_code=result.country_code,
        city_code="MSK",
        city_name="Moscow",
    )

    tasks = [
        asyncio.create_task(city_repository.create(cmd=cmd_1)),
        asyncio.create_task(city_repository.create(cmd=cmd_2)),
    ]

    with pytest.raises(CityNameAlreadyExists):
        await asyncio.gather(*tasks)
