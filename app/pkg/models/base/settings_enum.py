"""Module for environment enum model."""
from app.pkg.models.base import BaseEnum

__all__ = [
    "EnvironmentEnum",
]


class EnvironmentEnum(BaseEnum):
    """Enum for environment settings."""

    DEV = "dev"
    PROD = "prod"
