"""Configuration for pytest."""

import asyncio

import pytest

from app.configuration import __containers__
from app.pkg.connectors import Connectors
from app.pkg.connectors.postgresql import TestPostgresSQL

pytest_plugins = [
    "tests.fixtures.repository.postgresql.postgresql",
    "tests.fixtures.repository.postgresql.inserters",
    "tests.fixtures.router.client",
    "tests.fixtures.router.responses",
    "tests.fixtures.handlers.equals",
    "tests.fixtures.settings",
    "tests.v1.fixtures.repository.postgresql.repositories",
    "tests.v1.fixtures.repository.postgresql.inserters",
    "tests.v1.fixtures.services.services",
    "tests.v1.fixtures.services.city",
    # path to module with fixtures.
]

pytestmark = pytest.mark.anyio


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case.

    Notes:
        This fixture is used for anyio tests.

    Warnings:
        Full isolation for each test case is guaranteed only if the test cases
        are executed sequentially.
    """

    _ = request
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def pytest_sessionstart(session):
    _ = session
    __containers__.wire_packages(pkg_name="tests", unwire=True)
    Connectors.postgresql.override(TestPostgresSQL)
    __containers__.wire_packages(pkg_name="tests")
