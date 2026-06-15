GeoCompute Engine
FastAPI + PostGIS + Docker GIS Processing Backend

GeoCompute Engine ir konteinerizēts ģeotelpisko datu apstrādes serviss, kas nodrošina:

FastAPI backend ar modernu arhitektūru

PostGIS datubāzi ar automātisku inicializāciju

GeoJSON un Shapefile importu

Docker reproducējamību

GIS bibliotēku atbalstu (GDAL, PROJ, Fiona, GeoPandas, Shapely)

Alembic migrāciju sistēmu datubāzes shēmas pārvaldībai

Projekts ir pilnībā reproducējams no nulles — nepieciešams tikai Docker.

🚀 Run the project from scratch
1. Klonē repozitoriju
git clone https://github.com/girtsbeb-lab/GeoCompute-Engine.git  
cd GeoCompute-Engine

2. Startē visu stack (API + PostGIS)
docker compose down -v
docker compose up --build

Šis:

uzbūvē FastAPI image ar GDAL/PROJ atbalstu

palaiž PostGIS

automātiski izpilda app/db/init/*.sql

palaiž Alembic migrācijas

izveido tabulas

ieslēdz PostGIS extension

palaiž API uz porta 8000

3. Atver API dokumentāciju
http://localhost:8000/docs

Pieejamie endpointi:

/api/v1/import/geo — GIS failu imports

/api/v1/geo/... — ģeotelpiskie API

/health — veselības pārbaude

📦 Project Structure
GeoCompute-Engine/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── app/
│   ├── main.py
│   ├── db/
│   │   ├── init.py        # eksportē Base no session.py
│   │   ├── session.py         # SQLAlchemy Base + SessionLocal
│   │   └── init/
│   │       └── 01_init.sql
│   ├── api/
│   │   └── routes/
│   │       ├── geo.py
│   │       ├── health.py
│   │       └── import_geo.py
│   ├── models/
│   │   └── geodata.py
│   ├── services/
│   │   └── import_service.py
│   └── core/
│       └── config.py

🗄️ Database Auto‑Initialization
PostGIS tiek inicializēts automātiski, izmantojot:
app/db/init/01_init.sql

Fails izveido:

PostGIS extension

geodata tabulu

nepieciešamās privilēģijas

Tas notiek tikai pirmajā startā, kad tiek izveidots jauns Docker volume.

🧩 Alembic migrācijas
Projektā ir pievienota Alembic migrāciju sistēma datubāzes shēmas pārvaldībai.

Base importa konfigurācija
Alembic izmanto SQLAlchemy Base objektu no:
app/db/session.py

Lai Alembic varētu to importēt, failā app/db/init.py jābūt:
from .session import Base

Tas nodrošina, ka Alembic redz visus modeļus un var ģenerēt migrācijas.

🔄 Migrāciju komandas
Palaist visas migrācijas:
docker compose run --rm api alembic upgrade head

Izveidot jaunu migrāciju:
docker compose run --rm api alembic revision --autogenerate -m "Apraksts"

Atgriezties uz iepriekšējo migrāciju:
docker compose run --rm api alembic downgrade -1

🧪 Pārbaudīt, vai Alembic redz Base
docker compose run --rm --entrypoint sh api
python3 -c "from app.db import Base; print(Base)"

Pareizs rezultāts:
<class 'sqlalchemy.orm.decl_api.Base'>

🌍 GIS Import API
Endpoint
POST /api/v1/import/geo

Atbalstītie formāti
GeoJSON (.geojson, .json)

Shapefile (.shp)

Piemērs: GeoJSON imports
curl -X POST "http://localhost:8000/api/v1/import/geo" -F "file=@data.geojson"

Piemērs: Shapefile imports
curl -X POST "http://localhost:8000/api/v1/import/geo" -F "file=@layer.shp"

🧪 Verify imported data
docker exec -it geocompute-postgres psql -U geocompute -d geocompute -c "SELECT COUNT(*) FROM geodata;"
