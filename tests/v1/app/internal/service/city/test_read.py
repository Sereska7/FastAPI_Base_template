"""Test cases for CityService.read_city method."""

from app.internal.services.v1.city import CityService
from app.pkg.models.v1 import City, ReadCityByCountryQuery, ReadCityQuery


async def test_read_city(city_service: CityService):
    query = ReadCityQuery(city_id=1)
    expected_city = City(
        city_id=1,
        city_name="Test City",
        country_code="RUS",
        city_code="TCT",
    )
    city_service.city_repository.read.return_value = expected_city

    result = await city_service.read_city(query)

    assert result == expected_city
    city_service.city_repository.read.assert_called_once_with(query=query)


async def test_read_city_not_found(city_service: CityService):
    query = ReadCityQuery(city_id=1)
    city_service.city_repository.read.return_value = []

    assert await city_service.read_city(query) == []

    city_service.city_repository.read.assert_called_once_with(query=query)


async def test_read_cities_by_country(city_service: CityService):
    query = ReadCityByCountryQuery(
        country_code="RUS",
    )
    expected_cities = [
        City(city_id=1, city_name="Test City 1", country_code="RUS", city_code="TCT"),
        City(city_id=2, city_name="Test City 2", country_code="RUS", city_code="TCW"),
    ]
    city_service.city_repository.read_by_country.return_value = expected_cities

    result = await city_service.read_cities_by_country(query)

    assert result == expected_cities
    city_service.city_repository.read_by_country.assert_called_once_with(query=query)


async def test_read_all_cities(city_service: CityService):
    expected_cities = [
        City(city_id=1, city_name="Test City 1", country_code="RUS", city_code="TCT"),
        City(city_id=2, city_name="Test City 2", country_code="RUS", city_code="TCW"),
    ]
    city_service.city_repository.read_all.return_value = expected_cities

    result = await city_service.read_all_cities()

    assert result == expected_cities
    city_service.city_repository.read_all.assert_called_once()
