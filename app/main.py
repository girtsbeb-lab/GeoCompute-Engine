from fastapi import FastAPI

from app.api.routes.geo import router as geo_router
from app.api.routes.health import router as health_router
from app.api.routes.import_geo import router as import_router  # ← JAUNAIS IMPORTS
from app.core.config import get_settings
from app.db.session import init_db

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


# ROUTERI
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(geo_router, prefix="/api/v1/geo", tags=["geo"])
app.include_router(import_router, prefix="/api/v1/import", tags=["import"])  # ← JAUNAIS
