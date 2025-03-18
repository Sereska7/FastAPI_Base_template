"""Create fixtures for CityService tests."""

from unittest.mock import AsyncMock

import pytest

from app.internal.services.v1.city import CityService


@pytest.fixture
async def city_service():
    service = CityService()
    service.city_repository = AsyncMock()
    return service
