import asyncio
import os
import pytest

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.db.session import Base, get_async_session
from fastapi.testclient import TestClient
from app.main import app


TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL", "sqlite+aiosqlite:///./test.db")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    return engine


@pytest.fixture(scope="session", autouse=True)
async def prepare_database(db_engine):
    # create tables
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # teardown
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
def client(monkeypatch, db_engine):
    # create a sessionmaker bound to test engine and override dependency
    TestSession = async_sessionmaker(db_engine, expire_on_commit=False)

    async def _get_test_session():
        async with TestSession() as session:
            yield session

    monkeypatch.setattr(get_async_session.__module__, "get_async_session", _get_test_session)

    with TestClient(app) as c:
        yield c
