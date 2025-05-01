from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests import factories


async def test_get_stops_empty(client: AsyncClient, db_session: AsyncSession) -> None:
    factories.RouteModelFactory.__async_session__ = db_session
    route = await factories.RouteModelFactory.create_async()

    response = await client.get(f"/api/routes/{route.id}/stops/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["items"]) == 0

    response = await client.get("/api/stops/0/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_stops(client: AsyncClient, db_session: AsyncSession) -> None:
    factories.RouteModelFactory.__async_session__ = db_session
    factories.StopModelFactory.__async_session__ = db_session
    route = await factories.RouteModelFactory.create_async()
    stop = await factories.StopModelFactory.create_async(route_id=route.id)

    response = await client.get(f"/api/routes/{stop.route_id}/stops/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 1
    for k, v in data["items"][0].items():
        assert v == getattr(stop, k)


async def test_get_stop(client: AsyncClient, db_session: AsyncSession) -> None:
    factories.RouteModelFactory.__async_session__ = db_session
    factories.StopModelFactory.__async_session__ = db_session
    route = await factories.RouteModelFactory.create_async()
    stop = await factories.StopModelFactory.create_async(route_id=route.id)

    response = await client.get(f"/api/stops/{stop.id}/")
    assert response.status_code == status.HTTP_200_OK
    for k, v in response.json().items():
        assert v == getattr(stop, k)


async def test_get_stop_not_exist(client: AsyncClient) -> None:
    response = await client.get("/api/stops/999/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_create_stops(client: AsyncClient, db_session: AsyncSession) -> None:
    factories.RouteModelFactory.__async_session__ = db_session
    route = await factories.RouteModelFactory.create_async()

    stops_to_create = [factories.StopCreateSchemaFactory.build(), factories.StopCreateSchemaFactory.build()]
    response = await client.post(
        f"/api/routes/{route.id}/stops/",
        json=[x.model_dump() for x in stops_to_create],
    )
    assert response.status_code == status.HTTP_200_OK
    created_data = response.json()

    # check creation
    response = await client.get(f"/api/routes/{route.id}/stops/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert created_data == data
    assert len(data["items"]) == len(stops_to_create)
    for k, v in stops_to_create[0].model_dump().items():
        assert data["items"][0][k] == v
    for k, v in stops_to_create[1].model_dump().items():
        assert data["items"][1][k] == v

    # unique constraint error
    response = await client.post(
        f"/api/routes/{route.id}/stops/",
        json=[stops_to_create[0].model_dump(), stops_to_create[1].model_dump()],
    )
    data = response.json()
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert data["detail"] == "A record matching the supplied data already exists."


async def test_update_stops(client: AsyncClient, db_session: AsyncSession) -> None:
    factories.RouteModelFactory.__async_session__ = db_session
    factories.StopModelFactory.__async_session__ = db_session
    route = await factories.RouteModelFactory.create_async()
    stop1, stop2 = await factories.StopModelFactory.create_batch_async(size=2, route_id=route.id)

    updated_data = [
        {
            "id": stop1.id,
            "front": "stop front updated",
            "back": "stop back updated",
            "hint": "stop hint updated",
        },
        {
            "id": stop2.id,
            "front": "stop front2 updated",
            "back": "stop back2 updated",
            "hint": "stop hint2 updated",
        },
    ]
    response = await client.put(
        f"/api/routes/{route.id}/stops/",
        json=updated_data,
    )
    assert response.status_code == status.HTTP_200_OK
    stops = response.json()["items"]
    for x in stops:
        assert x.pop("route_id") == route.id
    assert stops == updated_data

    # check creation
    response = await client.get(f"/api/routes/{route.id}/stops/")
    assert response.status_code == status.HTTP_200_OK
    stops = response.json()["items"]
    assert len(stops) == len(updated_data)
    for x in stops:
        assert x.pop("route_id") == route.id
    assert stops == updated_data

