"""Routes for city module."""

from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.internal.pkg.middlewares.token_based_verification import (
    token_based_verification,
)
from app.internal.services import Services
from app.internal.services.v1.city import CityService
from app.pkg.models import v1 as models
from app.pkg.models.base.request_id_route import RequestIDRoute

router = APIRouter(
    prefix="/city",
    tags=["City"],
    route_class=RequestIDRoute,
)


@router.get(
    "/",
    response_model=List[models.City],
    status_code=status.HTTP_200_OK,
    description="""
    Description: Get all city.
    Used: Used in frontend.
    """,
    dependencies=[Depends(token_based_verification)],
)
@inject
async def read_all_city(
    city_service: CityService = Depends(Provide[Services.v1.city_service]),
):
    return await city_service.read_all_cities()


@router.get(
    "/{country_code:str}/",
    response_model=List[models.City],
    status_code=status.HTTP_200_OK,
    description="""
    Description: Read specific city.
    Used: Used in frontend.
    """,
)
@inject
async def read_city_by_country(
    country_code: str,
    city_service: CityService = Depends(Provide[Services.v1.city_service]),
):
    return await city_service.read_cities_by_country(
        query=models.ReadCityByCountryQuery(country_code=country_code),
    )


@router.post(
    "/",
    response_model=models.City,
    status_code=status.HTTP_201_CREATED,
    description="""
    Description: Create city.
    Used: Used in frontend.
    """,
    dependencies=[Depends(token_based_verification)],
)
@inject
async def create_city(
    cmd: models.CreateCityCommand,
    city_service: CityService = Depends(Provide[Services.v1.city_service]),
):
    return await city_service.create_city(cmd=cmd)


@router.put(
    "/",
    response_model=models.City,
    status_code=status.HTTP_200_OK,
    description="""
    Description: Update city - all data.
    Used: Used in frontend.
    """,
    dependencies=[Depends(token_based_verification)],
)
@inject
async def update_city_all(
    cmd: models.UpdateCityCommand,
    city_service: CityService = Depends(Provide[Services.v1.city_service]),
):
    return await city_service.update_city(cmd=cmd)


@router.patch(
    "/",
    response_model=models.City,
    status_code=status.HTTP_200_OK,
    description="""
    Description: Update city - not all data.
    Used: Used in frontend.
    """,
    dependencies=[Depends(token_based_verification)],
)
@inject
async def update_city(
    cmd: models.UpdateCityCommand,
    city_service: CityService = Depends(Provide[Services.v1.city_service]),
):
    return await city_service.update_city(cmd=cmd)


@router.delete(
    "/{city_id:int}/",
    response_model=models.City,
    status_code=status.HTTP_200_OK,
    description="""
    Description: Delete city.
    Used: Used in frontend.
    """,
    dependencies=[Depends(token_based_verification)],
)
@inject
async def delete_city(
    city_id: int,
    city_service: CityService = Depends(Provide[Services.v1.city_service]),
):
    return await city_service.delete_city(cmd=models.DeleteCityCommand(city_id=city_id))
