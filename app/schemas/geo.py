from typing import Any

from pydantic import BaseModel, Field


class GeoFeatureCreate(BaseModel):
    name: str = Field(..., max_length=255)
    geometry_type: str = Field(..., max_length=64)
    description: str | None = None
    geometry: dict[str, Any]


class GeoFeatureRead(BaseModel):
    id: int
    name: str
    geometry_type: str
    description: str | None = None
    geometry: dict[str, Any]

    model_config = {"from_attributes": True}
