-- Ieslēdz PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- Izveido tabulu, ja nav
CREATE TABLE IF NOT EXISTS geodata (
    id SERIAL PRIMARY KEY,
    name TEXT,
    geom geometry(Geometry, 4326)
);

-- Piešķir tiesības lietotājam
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO geocompute;
