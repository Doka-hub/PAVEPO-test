import asyncio
import os

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


@pytest.fixture(scope='session')
def settings():
    from app.config.settings import get_settings
    os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./test.db'
    os.environ['BASE_URL'] = 'http://testserver/api/v1'
    return get_settings()


@pytest.fixture(scope='session')
def app(settings):
    from app.config.app import create_app
    app = create_app(settings)
    yield app


@pytest.fixture(scope="session")
def engine(settings):
    eng = create_async_engine(settings.DATABASE_URL, echo=True)
    yield eng
    asyncio.run(eng.dispose())


@pytest.fixture(scope="session")
def async_session_maker(engine):
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db_tables(engine):
    from app.config.database import create_tables

    await create_tables(engine)


@pytest_asyncio.fixture(scope="function")
async def db(async_session_maker):
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
def client(app, settings):
    with TestClient(app, base_url=settings.BASE_URL) as ac:
        yield ac
