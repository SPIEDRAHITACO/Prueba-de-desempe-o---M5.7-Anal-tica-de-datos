-- Analytical views aligned to the business questions used in Power BI.
-- These views keep the dashboard layer simple and reusable.

CREATE OR REPLACE VIEW vw_sales_trend_monthly AS
SELECT
    df.year,
    df.month,
    SUM(f.sales) AS total_sales,
    COUNT(DISTINCT f.ordernumber) AS total_orders
FROM fact_ventas f
INNER JOIN dim_fecha df ON f.fecha_id = df.fecha_id
GROUP BY 1, 2
ORDER BY 1, 2;

CREATE OR REPLACE VIEW vw_sales_by_region AS
SELECT
    dg.continente,
    dg.region,
    dg.pais_oficial,
    SUM(f.sales) AS total_sales,
    COUNT(DISTINCT f.ordernumber) AS total_orders
FROM fact_ventas f
INNER JOIN dim_geografia dg ON f.geografia_id = dg.geografia_id
GROUP BY 1, 2, 3
ORDER BY total_sales DESC;

CREATE OR REPLACE VIEW vw_product_performance AS
SELECT
    d.producto_id,
    d.producto_nombre,
    d.categoria,
    SUM(f.sales) AS total_sales,
    SUM(f.quantityordered) AS total_units,
    COUNT(DISTINCT f.ordernumber) AS total_orders
FROM fact_ventas f
INNER JOIN dim_productos d ON f.producto_id = d.producto_id
GROUP BY 1, 2, 3
ORDER BY total_sales DESC;

CREATE OR REPLACE VIEW vw_low_performance_regions AS
SELECT *
FROM vw_sales_by_region
ORDER BY total_sales ASC
LIMIT 10;

CREATE OR REPLACE VIEW vw_customer_value AS
SELECT
    c.cliente_id,
    c.nombre,
    c.pais_normalizado,
    COUNT(DISTINCT f.ordernumber) AS frecuencia_pedidos,
    SUM(f.sales) AS revenue_total,
    AVG(f.sales) AS ticket_promedio,
    CASE
        WHEN SUM(f.sales) >= 50000 THEN 'High Value'
        WHEN SUM(f.sales) >= 20000 THEN 'Mid Value'
        ELSE 'Low Value'
    END AS value_segment
FROM fact_ventas f
INNER JOIN dim_clientes c ON f.cliente_id = c.cliente_id
GROUP BY 1, 2, 3;

CREATE OR REPLACE VIEW vw_geo_behavior AS
SELECT
    dg.continente,
    dg.region,
    dg.pais_oficial,
    AVG(f.sales) AS avg_line_sale,
    AVG(f.quantityordered) AS avg_units,
    AVG(f.priceeach) AS avg_price,
    COUNT(DISTINCT f.ordernumber) AS total_orders
FROM fact_ventas f
INNER JOIN dim_geografia dg ON f.geografia_id = dg.geografia_id
GROUP BY 1, 2, 3;
