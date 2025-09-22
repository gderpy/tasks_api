from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.version import router as version_router


def create_app() -> FastAPI:
    app = FastAPI(title="Tasks API")
    app.include_router(health_router, tags=["health"])
    app.include_router(version_router, tags=["version"])
    return app

app = create_app()