"""Module for testing read_all method in country repository."""

import pytest

from app.internal.repository.v1.postgresql import CountryRepository


@pytest.mark.postgresql
@pytest.mark.slow
async def test_read_all(
    country_repository: CountryRepository,
    country_inserter,
) -> None:

    result, _ = await country_inserter()

    assert await country_repository.read_all() == [result]


@pytest.mark.postgresql
@pytest.mark.slow
async def test_country_not_found(country_repository: CountryRepository) -> None:

    assert await country_repository.read_all() == []
