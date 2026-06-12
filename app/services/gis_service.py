from __future__ import annotations

import json
from typing import Any

import geopandas as gpd
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import shape
from sqlalchemy.orm import Session

from app.models.feature import GeoFeature
from app.schemas.geo import GeoFeatureCreate, GeoFeatureRead


class GISService:
    @staticmethod
    def create_feature(db: Session, payload: GeoFeatureCreate) -> GeoFeature:
        geometry = shape(payload.geometry)
        feature = GeoFeature(
            name=payload.name,
            geometry_type=payload.geometry_type,
            description=payload.description,
            geom=from_shape(geometry, srid=4326),
        )
        db.add(feature)
        db.commit()
        db.refresh(feature)
        return feature

    @staticmethod
    def list_features(db: Session) -> list[GeoFeatureRead]:
        features = db.query(GeoFeature).order_by(GeoFeature.id.asc()).all()
        return [GISService._to_read_model(feature) for feature in features]

    @staticmethod
    def get_feature(db: Session, feature_id: int) -> GeoFeatureRead | None:
        feature = db.query(GeoFeature).filter(GeoFeature.id == feature_id).first()
        if feature is None:
            return None
        return GISService._to_read_model(feature)

    @staticmethod
    def buffer_geometry(geometry: dict[str, Any], distance: float) -> dict[str, Any]:
        gdf = gpd.GeoDataFrame(geometry=[shape(geometry)], crs="EPSG:4326")
        buffered = gdf.geometry.buffer(distance).iloc[0]
        return json.loads(gpd.GeoSeries([buffered], crs="EPSG:4326").to_json())["features"][0]["geometry"]

    @staticmethod
    def _to_read_model(feature: GeoFeature) -> GeoFeatureRead:
        geometry = to_shape(feature.geom)
        return GeoFeatureRead(
            id=feature.id,
            name=feature.name,
            geometry_type=feature.geometry_type,
            description=feature.description,
            geometry=json.loads(gpd.GeoSeries([geometry], crs="EPSG:4326").to_json())["features"][0]["geometry"],
        )
