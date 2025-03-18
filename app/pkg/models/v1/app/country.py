"""Models for country object."""

import typing

from pydantic.fields import Field
from pydantic.types import PositiveInt

from app.pkg.models.base import BaseModel
from app.pkg.models.v1.app.city import City

__all__ = [
    "Country",
    "CountryFields",
    "CreateCountryCommand",
    "ReadCountryQuery",
    "UpdateCountryCommand",
    "DeleteCountryCommand",
    "CountryWithCities",
    "CreateCountyChangelogCommand",
]


class BaseCountry(BaseModel):
    """Base model for country."""


class CountryFields:
    """Fields for country model."""

    country_id: PositiveInt = Field(description="Internal skill id.", examples=[1])
    country_name: str = Field(
        description="Country name.",
        examples=["Russia"],
        min_length=1,
    )
    country_code: str = Field(
        description="Country code.",
        examples=["RUS"],
        min_length=3,
        pattern=r"^[A-Z]{3}$",
    )
    cities: typing.List[City] = Field(description="List of cities.")


class _Country(BaseCountry):
    country_name: str = CountryFields.country_name
    country_code: str = CountryFields.country_code


class Country(_Country):
    country_id: PositiveInt = CountryFields.country_id


# Commands.
class CreateCountryCommand(_Country): ...


class UpdateCountryCommand(_Country):
    country_id: PositiveInt = CountryFields.country_id


class DeleteCountryCommand(BaseCountry):
    country_id: PositiveInt = CountryFields.country_id


# Queries.
class ReadCountryQuery(BaseCountry):
    country_id: PositiveInt = CountryFields.country_id


class CountryWithCities(Country):
    cities: typing.List[City] = CountryFields.cities


class CreateCountyChangelogCommand(Country): ...
