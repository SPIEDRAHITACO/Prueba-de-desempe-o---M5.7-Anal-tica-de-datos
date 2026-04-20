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

CREATE TABLE IF NOT EXISTS dim_paises (
    pais_normalizado TEXT PRIMARY KEY,
    pais_oficial TEXT,
    continente TEXT,
    region TEXT,
    subregion TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    cca2 TEXT,
    cca3 TEXT
);

CREATE TABLE IF NOT EXISTS fact_ventas (
    venta_linea_id BIGINT PRIMARY KEY,
    ordernumber BIGINT,
    orderlinenumber INTEGER,
    orderdate TIMESTAMP,
    status TEXT,
    quantityordered DOUBLE PRECISION,
    priceeach DOUBLE PRECISION,
    sales DOUBLE PRECISION,
    qtr_id INTEGER,
    month_id INTEGER,
    year_id INTEGER,
    territory TEXT,
    dealsize TEXT,
    country TEXT,
    country_normalized TEXT,
    producto_id INTEGER REFERENCES dim_productos(producto_id),
    cliente_id INTEGER REFERENCES dim_clientes(cliente_id)
);
