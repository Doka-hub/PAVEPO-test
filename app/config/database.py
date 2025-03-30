from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def get_engine(url):
    return create_async_engine(url)


def get_sessionmaker(engine):
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db_session():
    from app.main import settings
    AsyncSessionLocal = get_sessionmaker(get_engine(settings.DATABASE_URL))

    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
