# GeoCompute Engine
FastAPI + PostGIS + Docker GIS Processing Backend

GeoCompute Engine ir konteinerizēts ģeotelpisko datu apstrādes serviss, kas nodrošina:

- FastAPI backend ar modernu arhitektūru
- PostGIS datubāzi ar automātisku inicializāciju
- GeoJSON un Shapefile importu
- Docker reproducējamību
- GIS bibliotēku atbalstu (GDAL, PROJ, Fiona, GeoPandas, Shapely)

Projekts ir pilnībā reproducējams no nulles — nepieciešams tikai Docker.

---

## 🚀 Run the project from scratch

### 1. Klonē repozitoriju

```bash
git clone https://github.com/girtsbeb-lab/GeoCompute-Engine.git
cd GeoCompute-Engine
```

### 2. Startē visu stack (API + PostGIS)

```bash
docker compose down -v
docker compose up --build
```

Šis:

- uzbūvē FastAPI image ar GDAL/PROJ atbalstu
- palaiž PostGIS
- automātiski izpilda `db/init/*.sql`
- izveido tabulas
- ieslēdz PostGIS extension
- palaiž API uz porta 8000

### 3. Atver API dokumentāciju

```
http://localhost:8000/docs
```

Pieejamie endpointi:

- `/api/v1/import/geo` — GIS failu imports
- `/api/v1/geo/...` — ģeotelpiskie API
- `/health` — veselības pārbaude

---

## 📦 Project Structure

```
GeoCompute-Engine/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── app/
│   ├── main.py
│   ├── db.py
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
└── db/
    └── init/
        └── 01_init.sql
```

---

## 🗄️ Database Auto‑Initialization

PostGIS tiek inicializēts automātiski, izmantojot:

```
db/init/01_init.sql
```

Fails izveido:

- PostGIS extension
- `geodata` tabulu
- nepieciešamās privilēģijas

Tas notiek tikai pirmajā startā, kad tiek izveidots jauns Docker volume.

---

## 🌍 GIS Import API

### Endpoint

```
POST /api/v1/import/geo
```

### Atbalstītie formāti

- GeoJSON (.geojson, .json)
- Shapefile (.shp)

### Piemērs: GeoJSON imports

```bash
curl -X POST "http://localhost:8000/api/v1/import/geo" \
  -F "file=@data.geojson"
```

### Piemērs: Shapefile imports

```bash
curl -X POST "http://localhost:8000/api/v1/import/geo" \
  -F "file=@layer.shp"
```

---

## 🧪 Verify imported data

```bash
docker exec -it geocompute-postgres \
  psql -U geocompute -d geocompute \
  -c "SELECT COUNT(*) FROM geodata;"
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| API | FastAPI |
| Database | PostGIS (PostgreSQL + GIS) |
| ORM | SQLAlchemy + GeoAlchemy2 |
| GIS libs | GeoPandas, Fiona, Shapely, pyproj |
| Runtime | Docker + docker-compose |
| Config | Pydantic Settings |

---

## 🐳 Docker Setup

### Dockerfile nodrošina:

- GDAL + PROJ instalāciju
- Fiona/GeoPandas atbalstu
- Python 3.11 slim image
- Uvicorn serveri

### docker-compose nodrošina:

- PostGIS servisu ar auto-init
- API servisu ar restart politiku
- Healthcheck DB servisam

---

## 🔧 Development commands

### Restartēt visu stack

```bash
docker compose down -v
docker compose up --build
```

### Restartēt tikai API

```bash
docker compose restart api
```

---

## 📌 Future improvements

- CSV imports
- GPX imports
- Alembic migrācijas
- Frontend karte (Leaflet / MapLibre)
- Background tasks lieliem failiem

---

## 👤 Author

Ģirts Bebrovskis  
Rīga, Latvija

---

## 📄 License

MIT License
