import typing

import fastapi
from advanced_alchemy.exceptions import NotFoundError
from modern_di_fastapi import FromDI
from sqlalchemy import orm
from starlette import status

from app import ioc, models, schemas
from app.repositories import RoutesService


ROUTER: typing.Final = fastapi.APIRouter()


def get_routes_service() -> RoutesService:
    return RoutesService()


@ROUTER.get("/routes/")
async def list_routes(
    routes_service: RoutesService = FromDI(ioc.Dependencies.routes_service),
) -> schemas.Routes:
    objects = await routes_service.list()
    return typing.cast("schemas.Routes", {"items": objects})


@ROUTER.get("/routes/{route_id}/")
async def get_route(
    route_id: int,
    routes_service: RoutesService = FromDI(ioc.Dependencies.routes_service),
) -> schemas.Route:
    instance = await routes_service.get_one_or_none(
        models.Route.id == route_id,
        load=[orm.selectinload(models.Route.cards)],
    )
    if not instance:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route is not found")

    return typing.cast("schemas.Route", instance)


@ROUTER.put("/routes/{route_id}/")
async def update_route(
    route_id: int,
    data: schemas.RouteCreate,
    routes_service: RoutesService = FromDI(ioc.Dependencies.routes_service),
) -> schemas.Route:
    try:
        instance = await routes_service.update(data=data.model_dump(), item_id=route_id)
    except NotFoundError:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route is not found") from None

    return typing.cast("schemas.Route", instance)


@ROUTER.post("/routes/")
async def create_route(
    data: schemas.RouteCreate,
    routes_service: RoutesService = FromDI(ioc.Dependencies.routes_service),
) -> schemas.Route:
    instance = await routes_service.create(data.model_dump())
    return typing.cast("schemas.Route", instance)
