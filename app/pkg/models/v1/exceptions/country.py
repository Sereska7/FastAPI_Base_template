"""Exceptions for a Country model."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = ["CountryNameAlreadyExists", "CountryCodeAlreadyExists", "CountryNotFound"]


class CountryNameAlreadyExists(BaseAPIException):
    message = "This 'name' of country already exists."
    status_code = status.HTTP_409_CONFLICT


class CountryCodeAlreadyExists(BaseAPIException):
    message = "This 'code' of country already exists."
    status_code = status.HTTP_409_CONFLICT


class CountryNotFound(BaseAPIException):
    message = "Country not found."
    status_code = status.HTTP_404_NOT_FOUND


__constrains__ = {
    "city_country_id_fkey": CountryNotFound,
    "country_country_name_key": CountryNameAlreadyExists,
    "country_country_code_key": CountryCodeAlreadyExists,
}
