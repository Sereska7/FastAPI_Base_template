"""Module for testing delete method in country repository."""

import pytest

from app.internal.repository.v1.postgresql import CountryRepository
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.repository import EmptyResult


@pytest.mark.postgresql
async def test_correct(country_repository: CountryRepository, country_inserter):
    result, _ = await country_inserter()
    cmd = result.migrate(model=models.DeleteCountryCommand)

    await country_repository.delete(cmd=cmd)

    with pytest.raises(EmptyResult):
        await country_repository.read(
            query=models.ReadCountryQuery(country_id=result.country_id),
        )


@pytest.mark.postgresql
async def test_country_not_found(
    country_repository: CountryRepository,
    country_inserter,
):
    result, _ = await country_inserter()
    cmd = models.DeleteCountryCommand.factory().build(country_id=result.country_id + 1)

    with pytest.raises(EmptyResult):
        await country_repository.delete(cmd=cmd)
