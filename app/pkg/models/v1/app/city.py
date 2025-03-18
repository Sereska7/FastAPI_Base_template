"""Models of city object."""

from pydantic import model_validator
from pydantic.fields import Field
from pydantic.types import PositiveInt, StrictStr

from app.pkg.models.base import BaseModel
from app.pkg.models.base.optional_field import OptionalField

__all__ = [
    "City",
    "CreateCityCommand",
    "ReadCityQuery",
    "ReadCityByCountryQuery",
    "UpdateCityCommand",
    "DeleteCityCommand",
]


class BaseCity(BaseModel):
    """Base model for city."""


class CityFields:
    """City fields."""

    city_id: PositiveInt = Field(description="Internal city id.", examples=[1])
    city_name: StrictStr = Field(
        description="City name.",
        examples=["Moscow"],
        min_length=1,
    )
    city_code: StrictStr = Field(
        description="City code.",
        examples=["MSK"],
        min_length=3,
        pattern=r"^[A-Z]{3}$",
    )
    country_code: StrictStr = Field(
        description="Country code.",
        examples=["RUS"],
        min_length=3,
    )


class OptionalCityFields:
    """Optional city fields."""

    city_name: StrictStr | None = OptionalField(CityFields.city_name)
    city_code: StrictStr | None = OptionalField(CityFields.city_code)
    country_code: StrictStr | None = OptionalField(CityFields.country_code)


class _City(BaseCity):
    city_name: StrictStr = CityFields.city_name
    city_code: StrictStr = CityFields.city_code
    country_code: StrictStr = CityFields.country_code


class City(_City):
    city_id: PositiveInt = CityFields.city_id


# Commands.
class CreateCityCommand(_City): ...


class UpdateCityCommand(BaseCity):
    """Update city command."""

    city_id: PositiveInt = CityFields.city_id
    city_name: StrictStr | None = OptionalCityFields.city_name
    city_code: StrictStr | None = OptionalCityFields.city_code
    country_code: StrictStr | None = OptionalCityFields.country_code

    @model_validator(mode="before")
    @classmethod
    def check_query(cls, values):  # pylint: disable=no-self-argument
        if (
            not values.get("city_name")
            and not values.get("city_code")
            and not values.get("country_id")
        ):
            raise ValueError("You must provide at least one value.")
        return values


class DeleteCityCommand(BaseCity):
    city_id: PositiveInt = CityFields.city_id


# Queries.
class ReadCityQuery(BaseCity):
    city_id: PositiveInt = CityFields.city_id


class ReadCityByCountryQuery(BaseCity):
    country_code: StrictStr = CityFields.country_code
