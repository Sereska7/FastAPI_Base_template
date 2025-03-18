"""Test cases for CityService.create_city method."""

from app.internal.services.v1.city import CityService
from app.pkg.models.v1 import City, CreateCityCommand


async def test_create_city(city_service: CityService):
    cmd = CreateCityCommand(city_name="Test City", country_code="RUS", city_code="TCT")
    expected_city = City(
        city_id=1,
        city_name="Test City",
        country_code="RUS",
        city_code="TCT",
    )
    city_service.city_repository.create.return_value = expected_city

    result = await city_service.create_city(cmd)

    assert result == expected_city
    city_service.city_repository.create.assert_called_once_with(cmd=cmd)
