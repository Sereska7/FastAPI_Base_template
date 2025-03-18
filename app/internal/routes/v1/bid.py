"""Consumer routes module."""

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status

from app.internal.services import Services
from app.internal.services.v1 import BidService
from app.pkg.models import v1 as models
from app.pkg.models.base.request_id_route import RequestIDRoute

router = APIRouter(
    prefix="/bid",
    tags=["Bid V1"],
    route_class=RequestIDRoute,
)


@router.post(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
    Description: Bid route."
    Used: Used in backend.
    """,
)
@inject
async def create_bid(
    cmd: models.CreateBidCommand,
    bid_service: BidService = Depends(Provide[Services.v1.bid_service]),
):
    await bid_service.create_bid(cmd)


@router.post(
    "/second",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
    Description: Bid route - create second queue."
    Used: Used in backend.
    """,
)
@inject
async def create_bid_second(
    cmd: models.CreateBidCommand,
    bid_service: BidService = Depends(Provide[Services.v1.bid_service]),
):
    await bid_service.create_bid_second(cmd)
