import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_get_routes_empty(client: AsyncClient) -> None:
    response = await client.get("/api/routes/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["items"]) == 0


@pytest.mark.parametrize(
    ("hashed", "departure_at", "arrival_at", "status_code"),
    [
        (None, None, None, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("abc123", "2025-01-01T08:00:00", "2025-01-01T10:00:00", status.HTTP_200_OK),
    ],
)
async def test_post_routes(
    client: AsyncClient,
    hashed: str,
    departure_at: str,
    arrival_at: str,
    status_code: int,
) -> None:
    response = await client.post(
        "/api/routes/",
        json={
            "hashed": hashed,
            "departure_at": departure_at,
            "arrival_at": arrival_at,
        },
    )
    assert response.status_code == status_code


async def test_put_routes_not_exist(client: AsyncClient) -> None:
    response = await client.put(
        "/api/routes/999",
        json={"hashed": "abc123", "departure_at": "2025-01-01T08:00:00", "arrival_at": "2025-01-01T10:00:00"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_route_not_exist(client: AsyncClient) -> None:
    response = await client.delete("/api/routes/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
