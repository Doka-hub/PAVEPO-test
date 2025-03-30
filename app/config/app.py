from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, Depends

from app.config import get_settings, Settings


def create_app(
    settings: Optional[Settings] = None,
    dependencies: Optional[List] = None,
) -> FastAPI:
    if settings is None:
        settings = get_settings()

    from app.database import create_tables, get_db_session, get_engine

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("Starting service...")
        engine = get_engine(settings.DATABASE_URL)
        await create_tables(engine)

        yield

        print("Shutting down...")
        await engine.dispose()

    if dependencies is None:
        dependencies = [Depends(get_db_session)]

    app = FastAPI(
        title="Tron Address Analyzer",
        lifespan=lifespan,
        dependencies=dependencies,
        openapi_url=f"/api/v1/openapi.json",
        docs_url=f"/api/v1/docs",
        redoc_url=f"/api/v1/redoc",
    )

    from app.api import info, logs
    app.include_router(info.router, prefix="/api/v1")
    app.include_router(logs.router, prefix="/api/v1")
    return app
