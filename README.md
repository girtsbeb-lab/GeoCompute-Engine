# GeoCompute-Engine

GeoCompute-Engine is a Python geospatial API built with FastAPI, PostgreSQL/PostGIS, SQLAlchemy, GeoAlchemy2, GeoPandas, and Shapely.

## Features

- FastAPI server with health and geospatial endpoints
- PostgreSQL with PostGIS extension initialized on container startup
- SQLAlchemy models backed by GeoAlchemy2 geometry columns
- GeoPandas and Shapely-based spatial processing helpers
- Docker Compose setup for API and database

## Project Structure

```text
app/
	api/
		routes/
	core/
	db/
	models/
	schemas/
	services/
db/
	init/
Dockerfile
docker-compose.yml
requirements.txt
```

## Run With Docker Compose

1. Copy the example environment file if you want local overrides.
2. Build and start the stack:

```bash
docker compose up --build
```

3. Open the API at `http://localhost:8000`.

## Example Endpoints

- `GET /health` - health check
- `POST /api/v1/geo/features` - create a GeoJSON feature
- `GET /api/v1/geo/features` - list saved features
- `GET /api/v1/geo/features/{feature_id}` - fetch a feature by id
- `POST /api/v1/geo/buffer` - buffer an input GeoJSON geometry

## Example Request

```bash
curl -X POST http://localhost:8000/api/v1/geo/buffer \
	-H 'Content-Type: application/json' \
	-d '{
		"geometry": {"type": "Point", "coordinates": [-73.9857, 40.7484]},
		"distance": 0.01
	}'
```
