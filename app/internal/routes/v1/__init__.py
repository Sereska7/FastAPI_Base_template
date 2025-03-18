"""Routes for version 1 of the API."""

from fastapi import APIRouter

from app.internal.routes.v1.bid import router as bid_router
from app.internal.routes.v1.city import router as city_router
from app.internal.routes.v1.country import router as country_router

router = APIRouter(
    prefix="/v1",
)

routes = [
    city_router,
    country_router,
    bid_router,
]

for route in routes:
    router.include_router(route)
