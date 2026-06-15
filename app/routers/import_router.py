from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.import_service import import_geojson, import_shapefile

router = APIRouter(prefix="/import", tags=["Import"])


@router.post("/geo")
async def import_geo_data(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    ext = file.filename.split(".")[-1].lower()

    if ext in ("geojson", "json"):
        count = import_geojson(db, file)
        return {"status": "ok", "type": "geojson", "imported": count}

    if ext == "shp":
        count = import_shapefile(db, file)
        return {"status": "ok", "type": "shapefile", "imported": count}

    return {"status": "error", "message": f"Unsupported file type: .{ext}"}
