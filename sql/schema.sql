-- PostgreSQL star schema for the Emausoft analytics project.
-- The model uses date, geography, product, and customer dimensions plus a sales fact table.

CREATE TABLE IF NOT EXISTS dim_fecha (
    fecha_id INTEGER PRIMARY KEY,
    fecha DATE NOT NULL UNIQUE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    day INTEGER,
    day_of_week INTEGER,
    week_of_year INTEGER
);

CREATE TABLE IF NOT EXISTS dim_geografia (
    geografia_id INTEGER PRIMARY KEY,
    pais_normalizado TEXT NOT NULL UNIQUE,
    pais_oficial TEXT,
    continente TEXT,
    region TEXT,
    subregion TEXT,
    territory TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    cca2 TEXT,
    cca3 TEXT
);

CREATE TABLE IF NOT EXISTS dim_productos (
    producto_id INTEGER PRIMARY KEY,
    producto_nombre TEXT NOT NULL UNIQUE,
    categoria TEXT
);

CREATE TABLE IF NOT EXISTS dim_clientes (
    cliente_id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    ciudad TEXT,
    pais TEXT,
    pais_normalizado TEXT
);

CREATE TABLE IF NOT EXISTS fact_ventas (
    venta_linea_id BIGINT PRIMARY KEY,
    ordernumber BIGINT,
    orderlinenumber INTEGER,
    status TEXT,
    quantityordered DOUBLE PRECISION,
    priceeach DOUBLE PRECISION,
    sales DOUBLE PRECISION,
    dealsize TEXT,
    fecha_id INTEGER REFERENCES dim_fecha(fecha_id),
    geografia_id INTEGER REFERENCES dim_geografia(geografia_id),
    producto_id INTEGER REFERENCES dim_productos(producto_id),
    cliente_id INTEGER REFERENCES dim_clientes(cliente_id)
);
