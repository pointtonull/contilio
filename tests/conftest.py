import typing

import fastapi
import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.application import build_app
from app.repositories import CardsService, DecksService
from app.settings import settings


@pytest.fixture(scope="session")
def engine() -> AsyncEngine:
    return create_async_engine(settings.database_uri, echo=False, future=True)


@pytest.fixture
async def connection(engine: AsyncEngine) -> typing.AsyncIterator[AsyncConnection]:
    async with engine.connect() as connection:
        transaction = await connection.begin()
        await connection.begin_nested()
        try:
            yield connection
        finally:
            if connection.in_transaction():
                await transaction.rollback()


@pytest.fixture
async def db_session(connection: AsyncConnection) -> typing.AsyncIterator[AsyncSession]:
    async_session_factory = sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    async with async_session_factory() as session:
        yield session


@pytest.fixture
async def app() -> typing.AsyncIterator[fastapi.FastAPI]:
    app_ = build_app()
    async with LifespanManager(app_):
        yield app_


@pytest.fixture
async def client(app: fastapi.FastAPI) -> typing.AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
def decks_service(db_session: AsyncSession) -> DecksService:
    return DecksService(session=db_session)


@pytest.fixture
def cards_service(db_session: AsyncSession) -> CardsService:
    return CardsService(session=db_session)
