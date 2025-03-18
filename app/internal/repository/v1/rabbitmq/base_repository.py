"""Create base rabbitmq repository."""

import json
from typing import Any

import aio_pika

from app.internal.repository.v1.rabbitmq.connection import get_connection

__all__ = ["BaseRepository"]


class BaseRepository:
    """Create rabbitmq repository."""

    @staticmethod
    async def create(
        message: Any,
        routing_key: str,
    ):
        async with get_connection() as channel:
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(message.to_dict()).encode("utf-8")),
                routing_key=routing_key,
            )
            return message
