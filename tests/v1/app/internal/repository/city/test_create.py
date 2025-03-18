"""Module for testing create city command."""

import asyncio

import pytest
from pydantic import ValidationError

from app.internal.repository.v1.postgresql.city import CityRepository
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.city import CityNameAlreadyExists, DuplicateCityCode


@pytest.mark.postgresql
async def test_correct(
    city_repository: CityRepository,
    country_inserter,
) -> None:
    result, _ = await country_inserter()
    cmd = models.CreateCityCommand.factory().build(country_code=result.country_code)
    city = await city_repository.create(cmd=cmd)

    assert isinstance(city, models.City)
    assert city == cmd.migrate(
        model=models.City,
        extra_fields={"city_id": city.city_id},
    )


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

    cmd_2 = cmd_1.copy()
    cmd_2.city_name = "Moscow"

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

    cmd_2 = cmd_1.copy()
    cmd_2.city_code = "MSK"

    tasks = [
        asyncio.create_task(city_repository.create(cmd=cmd_1)),
        asyncio.create_task(city_repository.create(cmd=cmd_2)),
    ]

    with pytest.raises(CityNameAlreadyExists):
        await asyncio.gather(*tasks)


@pytest.mark.parametrize(
    "code",
    [
        "MS",
        "MO",
        "SP",
        "M",
        "SS",
        "S",
        "SO",
    ],
)
async def test_code_length_equal_3(
    code: str,
) -> None:
    with pytest.raises(ValidationError):
        models.CreateCityCommand.factory().build(
            city_code=code,
        )
