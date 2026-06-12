from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.geo import GeoFeatureCreate, GeoFeatureRead
from app.services.gis_service import GISService

router = APIRouter()


@router.post("/features", response_model=GeoFeatureRead, summary="Create a geospatial feature")
def create_feature(payload: GeoFeatureCreate, db: Session = Depends(get_db)) -> GeoFeatureRead:
    feature = GISService.create_feature(db, payload)
    return GISService._to_read_model(feature)


@router.get("/features", response_model=list[GeoFeatureRead], summary="List geospatial features")
def list_features(db: Session = Depends(get_db)) -> list[GeoFeatureRead]:
    return GISService.list_features(db)


@router.get("/features/{feature_id}", response_model=GeoFeatureRead, summary="Get a geospatial feature")
def get_feature(feature_id: int, db: Session = Depends(get_db)) -> GeoFeatureRead:
    feature = GISService.get_feature(db, feature_id)
    if feature is None:
        raise HTTPException(status_code=404, detail="Feature not found")
    return feature


@router.post("/buffer", summary="Buffer a GeoJSON geometry")
def buffer_geometry(payload: dict[str, Any]) -> dict[str, Any]:
    geometry = payload.get("geometry")
    distance = payload.get("distance")
    if geometry is None or distance is None:
        raise HTTPException(status_code=400, detail="geometry and distance are required")
    return {"geometry": GISService.buffer_geometry(geometry, float(distance))}
