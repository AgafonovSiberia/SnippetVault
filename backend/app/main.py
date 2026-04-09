import logging
import os
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import get_api_router
from app.api.exception_handlers import domain_exception_handler
from app.application.common.exceptions import DomainException
from app.core.config import config
from app.di import create_container


def _setup_debugger() -> None:
    if os.getenv("DEBUG_MODE") != "1":
        return
    try:
        import pydevd
        pydevd.settrace(
            "host.docker.internal",
            port=5678,
            stdout_to_server=True,
            stderr_to_server=True,
            overwrite_prev_trace=True,
            suspend=False,
        )
    except Exception:
        pass


def create_app() -> FastAPI:
    _setup_debugger()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    container = create_container()

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        try:
            yield
        finally:
            await container.close()

    app = FastAPI(
        title=config.app.PROJECT_NAME,
        version="1.0.0",
        lifespan=lifespan,
        docs_url=f"{config.app.API_V1_STR}/docs",
        redoc_url=f"{config.app.API_V1_STR}/redoc",
        openapi_url=f"{config.app.API_V1_STR}/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.app.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    app.include_router(get_api_router(), prefix=config.app.API_V1_STR)
    setup_dishka(container, app)
    app.add_exception_handler(DomainException, domain_exception_handler)

    @app.get("/health", tags=["System"], include_in_schema=False)
    async def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
