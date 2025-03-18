"""Module for testing update method of country repository."""

import uuid

import pytest

from app.internal.repository.v1.postgresql import CountryRepository
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.country import (
    CountryCodeAlreadyExists,
    CountryNameAlreadyExists,
)
from app.pkg.models.v1.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_correct(
    country_repository: CountryRepository,
    country_inserter,
):
    result, _ = await country_inserter()
    cmd = result.migrate(model=models.UpdateCountryCommand)

    after_update = await country_repository.update(cmd=cmd)
    assert after_update == cmd.migrate(
        model=models.Country,
        extra_fields={"country_id": result.country_id},
    )


@pytest.mark.postgresql
async def test_country_not_found(
    country_repository: CountryRepository,
    country_inserter,
):
    result, _ = await country_inserter()
    cmd = models.UpdateCountryCommand.factory().build(country_id=result.country_id + 1)

    with pytest.raises(EmptyResult):
        await country_repository.update(cmd=cmd)


@pytest.mark.postgresql
async def test_unique_country_name(
    country_repository: CountryRepository,
    country_inserter,
):
    old_result, _ = await country_inserter()

    result, _ = await country_inserter()
    cmd = result.migrate(
        model=models.UpdateCountryCommand,
        extra_fields={"country_name": old_result.country_name},
    )

    with pytest.raises(CountryNameAlreadyExists):
        await country_repository.update(cmd=cmd)


@pytest.mark.postgresql
async def test_unique_country_code(
    country_repository: CountryRepository,
    country_inserter,
):
    old_result, _ = await country_inserter()
    result, _ = await country_inserter()
    cmd = result.migrate(
        model=models.UpdateCountryCommand,
        extra_fields={
            "country_code": old_result.country_code,
            "country_name": uuid.uuid4().hex,
        },
    )

    with pytest.raises(CountryCodeAlreadyExists):
        await country_repository.update(cmd=cmd)


@pytest.mark.postgresql
@pytest.mark.repeat(5)
async def test_unique_country_code_and_name(
    country_repository: CountryRepository,
    country_inserter,
):
    old_result, _ = await country_inserter()
    new_result, _ = await country_inserter()
    cmd = old_result.migrate(
        model=models.UpdateCountryCommand,
        extra_fields={"country_id": new_result.country_id},
    )

    with pytest.raises(CountryNameAlreadyExists):
        await country_repository.update(cmd=cmd)


@pytest.mark.postgresql
@pytest.mark.parametrize(
    "country_name",
    [
        "Russia",
        "Russia ",
        " Russia",
        " Russia ",
        "Russia  ",
        "  Russia",
    ],
)
async def test_strip_whitespace_country_name(
    country_name: str,
):
    cmd = models.UpdateCountryCommand.factory().build(country_name=country_name)

    assert cmd.country_name == country_name.strip()
