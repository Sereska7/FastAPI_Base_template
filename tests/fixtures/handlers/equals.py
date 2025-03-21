"""Fixtures for the equals handler tests."""

import typing

import pytest


@pytest.fixture
def check_array_equality() -> (
    typing.Callable[[typing.List[typing.Any], typing.List[typing.Any]], bool]
):
    def wrapped(
        actual: typing.List[typing.Any],
        expected: typing.List[typing.Any],
    ) -> bool:
        return all(a in expected for a in actual)

    return wrapped


@pytest.fixture
def check_data_in_array() -> (
    typing.Callable[[typing.Any, typing.List[typing.Any]], bool]
):
    """Проверяем, есть ли нужное значение в массиве."""

    def wrapped(
        data_to_check: typing.Any,
        expected: typing.List[typing.Any],
    ) -> bool:
        return data_to_check in expected

    return wrapped
