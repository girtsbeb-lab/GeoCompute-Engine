from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String

from app.db import Base


class GeoData(Base):
    __tablename__ = "geodata"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    geom = Column(Geometry("GEOMETRY", srid=4326))
