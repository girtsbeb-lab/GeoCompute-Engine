FROM python:3.11-slim

# -----------------------------
# 1. Sistēmas konfigurācija
# -----------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# -----------------------------
# 2. GIS bibliotēkas (GDAL/PROJ)
# -----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    proj-bin \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# GDAL include ceļi (ļoti svarīgi Fiona/pyproj)
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# -----------------------------
# 3. Python atkarības
# -----------------------------
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# -----------------------------
# 4. Alembic konfigurācija
# -----------------------------
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic

# -----------------------------
# 5. Projekta failsistēma
# -----------------------------
COPY app ./app
COPY db/init ./db/init
COPY README.md ./README.md

EXPOSE 8000

# -----------------------------
# 6. Starta komanda (Alembic + API)
# -----------------------------
CMD sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"
