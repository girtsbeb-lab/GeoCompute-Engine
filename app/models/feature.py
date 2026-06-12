from sqlalchemy import Column, Integer, String, Text
from geoalchemy2 import Geometry

from app.db.session import Base


class GeoFeature(Base):
    __tablename__ = "geo_features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    geometry_type = Column(String(64), nullable=False)
    description = Column(Text, nullable=True)
    geom = Column(Geometry(geometry_type="GEOMETRY", srid=4326, spatial_index=True), nullable=False)
