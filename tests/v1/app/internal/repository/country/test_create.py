"""Module for testing create country command."""

import asyncio

import pytest
from pydantic import ValidationError

from app.internal.repository.v1.postgresql import CountryRepository
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.country import (
    CountryCodeAlreadyExists,
    CountryNameAlreadyExists,
)


@pytest.mark.postgresql
@pytest.mark.parametrize(
    "country_code",
    [
        "RUS",
        "USA",
    ],
)
async def test_correct(
    country_repository: CountryRepository,
    country_code,
):
    cmd = models.CreateCountryCommand.factory().build(country_code=country_code)

    result = await country_repository.create(cmd=cmd)
    assert result == cmd.migrate(
        model=models.Country,
        extra_fields={"country_id": result.country_id},
    )


@pytest.mark.postgresql
@pytest.mark.parametrize(
    "country_name",
    [
        "Russia",
        "USA",
    ],
)
async def test_unique_country_name(
    country_repository: CountryRepository,
    country_name: str,
):
    commands = []
    for _ in range(2):
        cmd = models.CreateCountryCommand.factory().build(country_name=country_name)
        commands.append(asyncio.create_task(country_repository.create(cmd=cmd)))

    with pytest.raises(CountryNameAlreadyExists):
        await asyncio.gather(*commands)


@pytest.mark.parametrize(
    "country_name",
    [
        "Russia",
        " Russia",
        "Russia ",
        " Russia ",
        "Russia  ",
        "  Russia",
    ],
)
async def test_strip_whitespace_country_name(
    country_name: str,
):
    cmd = models.CreateCountryCommand.factory().build(country_name=country_name)
    assert cmd.country_name == country_name.strip()


@pytest.mark.parametrize(
    "country_code",
    [
        "RUS",
        " RUS",
        "RUS ",
        " RUS ",
        "RUS  ",
        "  RUS",
    ],
)
async def test_strip_whitespace_country_code(
    country_code: str,
):
    cmd = models.CreateCountryCommand.factory().build(country_code=country_code)
    assert cmd.country_code == country_code.strip()


@pytest.mark.postgresql
@pytest.mark.parametrize(
    "country_code",
    [
        "RUS",
        "USA",
        "CAN",
        "CHN",
        "JPN",
        "DEU",
        "FRA",
        "ITA",
    ],
)
async def test_country_code_already_exists(
    country_repository: CountryRepository,
    country_code: str,
):
    commands = []
    for _ in range(2):
        cmd = models.CreateCountryCommand.factory().build(country_code=country_code)
        commands.append(asyncio.create_task(country_repository.create(cmd=cmd)))

    with pytest.raises(CountryCodeAlreadyExists):
        await asyncio.gather(*commands)


@pytest.mark.parametrize(
    "country_code",
    [
        "RU",
        "US",
        "CA",
        "CN",
        "JP",
        "DE",
        "FR",
        "IT",
        "AF",
        "AL",
        "DZ",
        "AS",
    ],
)
async def test_country_code_length(
    country_code: str,
):
    with pytest.raises(ValidationError):
        models.CreateCountryCommand.factory().build(country_code=country_code)
