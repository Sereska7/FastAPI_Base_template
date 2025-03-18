"""Models of bid object."""

from pydantic.fields import Field
from pydantic.types import PositiveInt

from app.pkg.models.base import BaseModel

__all__ = [
    "Bid",
    "CreateBidCommand",
]


class BaseBid(BaseModel):
    """Base model for bid."""


class BidFields:
    """Bid fields."""

    bid_name: PositiveInt = Field(
        description="Bid name.",
        examples=["bid_name"],
        min_length=1,
    )


class _Bid(BaseBid):
    bid_name: str = BidFields.bid_name


class Bid(_Bid): ...


# Commands.
class CreateBidCommand(_Bid): ...
