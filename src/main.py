from textwrap import dedent

from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.routes import ROUTER
from src.analyzers.base import AnalyserRegistry, register_analyzers
from src.settings import Settings
from src.helpers import (
    configure_logging,
    log_request_middleware,
    add_process_time_header,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    registry = AnalyserRegistry()
    register_analyzers(registry)
    app.state.registry = registry
    yield


def create_app() -> FastAPI:
    """Create a FastAPI application."""

    app = FastAPI(
        title="String Analysis API",
        summary="Analyse strings using NLP",
        version="v1",  # a fancier version would read the semver from pkg metadata
        description=dedent("""\
        Maintained by: abc@gmail.com

        | Helpful Links | Notes |
        | --- | --- |
        | [Confluence](https://example.com) | |
        """),
        lifespan=lifespan,
    )
    app.middleware("http")(log_request_middleware)
    app.middleware("http")(add_process_time_header)

    app.include_router(ROUTER)

    return app


if __name__ == "__main__":
    import uvicorn

    settings = Settings()
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=settings.port)
