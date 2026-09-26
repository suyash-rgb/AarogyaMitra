-- sql/schema.sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Kendra Spatial Store
CREATE TABLE IF NOT EXISTS jan_aushadhi_kendras (
    kendra_id VARCHAR(50) PRIMARY KEY,
    kendra_name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    district VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    phone VARCHAR(50),
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    geom GEOGRAPHY(Point, 4326)
);

CREATE INDEX IF NOT EXISTS idx_kendras_geom ON jan_aushadhi_kendras USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_kendras_pincode ON jan_aushadhi_kendras(pincode);

-- Generic Salt Substitution Store
CREATE TABLE IF NOT EXISTS medicine_master (
    id SERIAL PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL,
    generic_salt_name VARCHAR(255) NOT NULL,
    dosage_form VARCHAR(100),
    brand_mrp NUMERIC(10, 2) NOT NULL,
    jan_aushadhi_mrp NUMERIC(10, 2) NOT NULL,
    savings_percentage NUMERIC(5, 2) GENERATED ALWAYS AS (
        ROUND(((brand_mrp - jan_aushadhi_mrp) / brand_mrp) * 100, 2)
    ) STORED
);

CREATE INDEX IF NOT EXISTS idx_med_brand_trgm ON medicine_master USING GIN (brand_name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_med_salt_trgm ON medicine_master USING GIN (generic_salt_name gin_trgm_ops);
