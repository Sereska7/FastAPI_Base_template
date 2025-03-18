"""Module for testing read method of country repository."""

import pytest

from app.internal.repository.v1.postgresql import CountryRepository
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.repository import EmptyResult


@pytest.mark.postgresql
@pytest.mark.parametrize(
    "country_code",
    [
        "RUS",
        "USA",
    ],
)
async def test_correct(country_code, country_inserter):
    result, cmd = await country_inserter(country_code=country_code)

    assert result == cmd.migrate(
        model=models.Country,
        extra_fields={"country_id": result.country_id},
    )


@pytest.mark.postgresql
async def test_country_not_found(
    country_repository: CountryRepository,
    country_inserter,
):
    result, _ = await country_inserter()

    query = models.ReadCountryQuery.factory().build(country_id=result.country_id + 1)

    with pytest.raises(EmptyResult):
        await country_repository.read(query=query)
