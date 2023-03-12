import asyncio
from typing import AsyncGenerator
from app.api.deps import get_session
from app.main import app
from app.db.base_class import Base
from fastapi.testclient import TestClient
from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from faker import Faker
import pytest

from app import schemas


SQLALCHEMY_DATABASE_URL = PostgresDsn.build(
    scheme="postgresql+asyncpg",
    user="postgres",
    password="postgres",
    host="db",
    port="5432",
    path="/test",
)

test_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, future=True, poolclass=NullPool
)
TestingSessionLocal = sessionmaker(
    test_engine, autoflush=False, expire_on_commit=False, class_=AsyncSession
)


async def init_models():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_models())


async def override_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
        await session.close()


app.dependency_overrides[get_session] = override_session


@pytest.fixture(name="test_client", scope="function")
def fixture_test_client():
    yield TestClient(app)


@pytest.fixture(name="train_station")
def fixture_train_station():
    yield schemas.core.TrainStationSchema(
        id="ew21/cc22", name="Buona Vista", interchange=True
    )


@pytest.fixture(name="train_station_2")
def fixture_train_station_2():
    yield schemas.core.TrainStationSchema(
        id="ew20", name="Commonwealth", interchange=False
    )


@pytest.fixture(name="train_station_3")
def fixture_train_station_3():
    yield schemas.core.TrainStationSchema(
        id="ew19", name="Queenstown", interchange=False
    )


@pytest.fixture(name="station_to_be_replaced")
def fixture_station_to_be_replaced():
    yield schemas.core.TrainStationSchema(
        id="ew17", name="Tiong Bahru", interchange=False
    )


@pytest.fixture(name="connecting_station")
def fixture_connecting_station():
    yield schemas.core.ConnectingStationSchema(
        id="ew21/cc22", connecting_id="ew20", distance=3, transit_time=0
    )


@pytest.fixture(name="connecting_station_2")
def fixture_connecting_station_2():
    yield schemas.core.ConnectingStationSchema(
        id="ew20", connecting_id="ew19", distance=3, transit_time=0
    )
