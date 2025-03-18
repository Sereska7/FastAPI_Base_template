"""Container with rabbitmq consumer."""

from dependency_injector import containers, providers

from app.internal.repository import Repositories
from app.internal.repository.v1 import rabbitmq
from app.internal.services import Services
from app.pkg.settings import settings

__all__ = ["Workers"]


class Workers(containers.DeclarativeContainer):
    """Consumers container."""

    configuration = providers.Configuration(name="settings")
    configuration.from_dict(settings.model_dump())

    services: Services = providers.Container(Services)

    rabbitmq_repositories: rabbitmq.Repositories = providers.Container(
        Repositories.v1.rabbitmq,
    )  # type: ignore
