"""Routers for CRUD of countries."""

from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.internal.pkg.middlewares.token_based_verification import (
    token_based_verification,
)
from app.internal.services import Services
from app.internal.services.v1.country import CountryService
from app.pkg.models import v1 as models
from app.pkg.models.base.request_id_route import RequestIDRoute

router = APIRouter(
    prefix="/country",
    tags=["Country"],
    route_class=RequestIDRoute,
)


@router.get(
    "/",
    response_model=List[models.Country],
    status_code=status.HTTP_200_OK,
    description="""
    Description: Get all country.
    Used: Used in frontend.
    """,
)
@inject
async def read_all_country(
    country_service: CountryService = Depends(Provide[Services.v1.country_service]),
) -> List[models.Country]:
    return await country_service.read_all_countries()


@router.get(
    "/with_cities/",
    response_model=List[models.CountryWithCities],
    status_code=status.HTTP_200_OK,
    description="""
    Description: Get all country with cities.
    Used: This method is used as an example of injecting one service into another.
    """,
)
@inject
async def read_country_with_cities(
    country_service: CountryService = Depends(Provide[Services.v1.country_service]),
) -> List[models.CountryWithCities]:
    return await country_service.read_country_with_cities()


@router.get(
    "/{country_id:int}/",
    response_model=models.Country,
    status_code=status.HTTP_200_OK,
    description="""
    Description: Read specific country.
    Used: Used in frontend.
    """,
    dependencies=[Depends(token_based_verification)],
)
@inject
async def read_country(
    country_id: int,
    country_service: CountryService = Depends(Provide[Services.v1.country_service]),
) -> models.Country:
    return await country_service.read_country(
        query=models.ReadCountryQuery(country_id=country_id),
    )


@router.post(
    "/",
    response_model=models.Country,
    status_code=status.HTTP_201_CREATED,
    description="""
    Description: Create country.
    Used: Used in frontend.
    """,
    dependencies=[Depends(token_based_verification)],
)
@inject
async def create_country(
    cmd: models.CreateCountryCommand,
    country_service: CountryService = Depends(Provide[Services.v1.country_service]),
) -> models.Country:
    return await country_service.create_country(cmd=cmd)


@router.put(
    "/",
    response_model=models.Country,
    status_code=status.HTTP_200_OK,
    description="""
    Description: Update country.
    Used: Used in frontend.
    """,
    dependencies=[Depends(token_based_verification)],
)
@inject
async def update_country(
    cmd: models.UpdateCountryCommand,
    country_service: CountryService = Depends(Provide[Services.v1.country_service]),
) -> models.Country:
    return await country_service.update_country(cmd=cmd)


@router.delete(
    "/{country_id:int}/",
    response_model=models.Country,
    status_code=status.HTTP_200_OK,
    description="""
    Description: Delete country.
    Used: Used in frontend.
    """,
    dependencies=[Depends(token_based_verification)],
)
@inject
async def delete_country(
    country_id: int,
    country_service: CountryService = Depends(Provide[Services.v1.country_service]),
) -> models.Country:
    return await country_service.delete_country(
        cmd=models.DeleteCountryCommand(country_id=country_id),
    )
