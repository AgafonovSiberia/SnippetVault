import logging
import os
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.exception_handlers import domain_exception_handler
from app.application.common.exceptions import DomainException

from app.api import get_api_router
from app.di import create_container

API_PREFIX = '/api/'


if os.getenv("DEBUG_MODE") == "1":
    import pydevd

    try:
        pydevd.settrace(
            "host.docker.internal",
            port=5678,
            stdout_to_server=True,
            stderr_to_server=True,
            overwrite_prev_trace=True,
            suspend=False,
        )
    except TimeoutError:
        pass
    except Exception:
        pass

ORIGINS = [
    "https://localhost:5173",
    "https://127.0.0.1:5173",
    "http://localhost:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]


def create_app() -> FastAPI:
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

    from app.core.config import config

    fastapi = FastAPI(title="SnippetVault",
                      version="1.0.0",
                      lifespan=lifespan,
                      docs_url=f"{config.app.API_V1_STR}/docs",
                      redoc_url=f"{config.app.API_V1_STR}/redoc",
                      openapi_url=f"{config.app.API_V1_STR}/openapi.json")

    fastapi.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    fastapi.include_router(get_api_router(), prefix=config.app.API_V1_STR)
    setup_dishka(container, fastapi)

    fastapi.add_exception_handler(DomainException, domain_exception_handler)

    return fastapi


app = create_app()
