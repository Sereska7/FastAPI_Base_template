"""V1 service layer."""

from dependency_injector import containers, providers

from app.internal.repository import Repositories
from app.internal.repository.v1 import postgresql, rabbitmq
from app.internal.services.v1.bid import BidService
from app.internal.services.v1.city import CityService
from app.internal.services.v1.country import CountryService
from app.pkg.settings import settings


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    configuration = providers.Configuration(name="settings")
    configuration.from_dict(settings.model_dump())

    rabbitmq_repositories: rabbitmq.Repositories = providers.Container(
        Repositories.v1.rabbitmq,
    )  # type: ignore

    postgres_repositories: postgresql.Repositories = providers.Container(
        Repositories.v1.postgres,
    )  # type: ignore

    # CityService
    city_service = providers.Factory(
        CityService,
    )
    city_service.add_attributes(
        city_repository=postgres_repositories.city_repository,
    )

    # CountryService
    country_service = providers.Factory(
        CountryService,
    )
    country_service.add_attributes(
        country_repository=postgres_repositories.country_repository,
        city_service=city_service,
    )

    # BidService
    bid_service = providers.Factory(
        BidService,
    )
    bid_service.add_attributes(
        rabbit_base_repository=rabbitmq_repositories.base_repository,
        rabbit_bid_queue=configuration.RABBITMQ.BID_QUEUE_NAME,
        rabbit_bid_queue_second=configuration.RABBITMQ.BID_QUEUE_NAME_SECOND,
    )
