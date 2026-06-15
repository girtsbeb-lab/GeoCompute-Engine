import json
import tempfile
from pathlib import Path

import fiona
from shapely.geometry import shape
from sqlalchemy.orm import Session

from app.models.geodata import GeoData


def import_geojson(db: Session, upload_file):
    data = json.load(upload_file.file)

    features = data.get("features", [])
    count = 0

    for f in features:
        geom = shape(f["geometry"])
        props = f.get("properties", {})

        db_obj = GeoData(
            name=props.get("name"),
            geom=f"SRID=4326;{geom.wkt}",
        )
        db.add(db_obj)
        count += 1

    db.commit()
    return count


def import_shapefile(db: Session, upload_file):
    # saglabā uz diska, jo fiona strādā ar failiem
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        shp_path = tmpdir_path / upload_file.filename

        with shp_path.open("wb") as f:
            f.write(upload_file.file.read())

        count = 0
        with fiona.open(shp_path) as src:
            for feature in src:
                geom = shape(feature["geometry"])
                props = feature["properties"]

                db_obj = GeoData(
                    name=props.get("name"),
                    geom=f"SRID=4326;{geom.wkt}",
                )
                db.add(db_obj)
                count += 1

        db.commit()
        return count
