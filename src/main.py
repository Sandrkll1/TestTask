from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1 import setup
from src.di import Container


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await app.container.db().initialize_database()
    await app.container.redis_pool()
    yield


def create_app() -> FastAPI:
    ordinals = ["*"]
    container = Container()

    app = FastAPI(
        lifespan=lifespan,
        title="TestTask",
        root_path="/api"
    )

    app.container = container
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ordinals,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup(app)
    return app


app = create_app()
