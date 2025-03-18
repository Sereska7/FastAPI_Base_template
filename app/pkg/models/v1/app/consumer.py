"""Models of consumer object."""

from typing import Callable, Type

from pydantic.fields import Field

from app.pkg.models.base import BaseModel

__all__ = [
    "ConsumerQueueData",
]


class BaseConsumer(BaseModel):
    """Base model for bid."""


class ConsumerFields:
    """Bid fields."""

    queue_name: str = Field(title="Queue name.", examples=["mail"])
    queue_callback: Callable = Field(title="Callback function.", examples=["send_mail"])
    queue_incoming_model: BaseModel = Field(
        title="Incoming model.",
        examples=["CreateMailCommand"],
    )


class ConsumerQueueData(BaseConsumer):
    queue_name: str = ConsumerFields.queue_name
    queue_callback: Callable = ConsumerFields.queue_callback
    queue_incoming_model: Type[BaseModel] = ConsumerFields.queue_incoming_model
