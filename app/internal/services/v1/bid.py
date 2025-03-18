"""Module for consumer service."""

import asyncio

from app.internal.repository.v1.rabbitmq import BaseRepository
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models

__all__ = ["BidService"]


class BidService:
    """Consumer service."""

    rabbit_base_repository: BaseRepository
    rabbit_bid_queue: str
    rabbit_bid_queue_second: str

    def __init__(self):
        self.__logger = get_logger(__name__)

    async def create_bid(self, cmd: models.CreateBidCommand) -> None:
        """Create bid and send it to rabbit."""

        await self.rabbit_base_repository.create(
            message=cmd,
            routing_key=self.rabbit_bid_queue,
        )
        self.__logger.info("Message was sent to rabbitmq consumer queue.")

    async def bid_callback(self, cmd: models.CreateBidCommand) -> None:
        self.__logger.info("Bid callback was called with data %s.", cmd.to_dict())

    async def create_bid_second(self, cmd: models.CreateBidCommand) -> None:
        """Create bid and send it to rabbit - another queue."""

        await self.rabbit_base_repository.create(
            message=cmd,
            routing_key=self.rabbit_bid_queue_second,
        )
        self.__logger.info("Message was sent to rabbitmq consumer queue.")

    async def bid_callback_second(self, cmd: models.CreateBidCommand) -> None:
        self.__logger.info(
            "Bid callback second was called with data %s.",
            cmd.to_dict(),
        )
        await asyncio.sleep(60)
        self.__logger.info("End rabbit callback - bid second.")
