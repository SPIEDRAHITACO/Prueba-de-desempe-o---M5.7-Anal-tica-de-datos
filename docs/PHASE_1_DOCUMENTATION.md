<!-- Phase 1 evidence and technical summary. Use this as the handoff point before building Power BI. -->

# Phase 1 Technical Documentation

## 1. Scope

Phase 1 covers data ingestion, profiling, enrichment through APIs, dimensional modeling, PostgreSQL loading, and export-ready analytical outputs.

## 2. Delivered Components

### 2.1 Pipeline scripts

- `src/00_create_database.py`: Creates the target PostgreSQL database if missing.
- `src/01_ingest_and_profile.py`: Ingests CSV source, normalizes columns, profiles data quality.
- `src/02_build_customers_api.py`: Pulls synthetic customers from RandomUser API.
- `src/03_build_regions_api.py`: Pulls geographic metadata from RestCountries API.
- `src/04_build_products.py`: Builds product dimension from unique product codes.
- `src/05_integrate_and_load_pg.py`: Builds dimensions and fact table, loads PostgreSQL, creates views.
- `src/06_export_powerbi_views.py`: Exports `vw_*` views to CSV for Power BI.
- `src/run_pipeline.py`: Full end-to-end runner for all steps.

### 2.2 SQL assets

- `sql/schema.sql`: 5-table star schema DDL.
- `sql/analytics_views.sql`: Analytical views used by reporting.

### 2.3 Outputs

- Processed datasets in `outputs/processed/`.
- Data quality reports in `outputs/reports/`.
- Integration validation in `outputs/processed/integration_report.csv`.
- Power BI extracts in `outputs/processed/powerbi_*.csv`.

## 3. Final Data Model (Star Schema)

### 3.1 Dimension tables

- `dim_fecha`
  - Grain: one row per calendar date present in sales.
  - Key: `fecha_id`.
  - Attributes: date breakdown (year, quarter, month, day, weekday, ISO week).

- `dim_geografia`
  - Grain: one row per normalized country.
  - Key: `geografia_id`.
  - Attributes: country names, continent, region, subregion, territory, lat/long, CCA2, CCA3.

- `dim_productos`
  - Grain: one row per unique product code.
  - Key: `producto_id`.
  - Attributes: product code and product line category.

- `dim_clientes`
  - Grain: one row per generated customer.
  - Key: `cliente_id`.
  - Attributes: name, city, country, normalized country.

### 3.2 Fact table

- `fact_ventas`
  - Grain: one row per sales line.
  - Key: `venta_linea_id`.
  - Measures: `sales`, `quantityordered`, `priceeach`.
  - Foreign keys: `fecha_id`, `geografia_id`, `producto_id`, `cliente_id`.

## 4. Data Quality and Profiling Summary

Source file: `docs/sales_data_sample.csv`

Key metrics from profiling:

- Rows: 2823
- Columns: 26
- Duplicate rows: 0
- Invalid order dates: 0
- Inconsistent sales rows: 1304
- Critical field null rates: 0% on all required columns

Interpretation:

- Data is complete enough for dimensional loading.
- Sales formula inconsistencies are documented and intentionally preserved as observed transactional values.

## 5. Customer Assignment Strategy

Sales data does not include a native customer identifier.

Implemented logic:

1. Match by normalized country whenever possible.
2. If no country candidates exist, assign randomly from all customers using seeded RNG.

Current result in integration report:

- Country-based match rate: 85.3%
- Fallback rate: 14.7%

This guarantees full fact coverage while keeping geographic coherence as high as possible.
Because customers are generated from a live API, these percentages may vary slightly across executions.

## 6. Phase 1 Validation Evidence

From `outputs/processed/integration_report.csv`:

- `rows_fact_ventas`: 2823
- `rows_dim_fecha`: 252
- `rows_dim_geografia`: 250
- `rows_dim_productos`: 109
- `rows_dim_clientes`: 100

From execution status:

- PostgreSQL load: successful
- View creation: successful
- CSV exports: successful for all `vw_*` views

## 7. What Was Missing and Is Now Addressed

The following gaps were detected and closed:

1. README mismatch with implemented schema (old 4-table model).
2. Full runner did not include database creation step.
3. No dedicated Phase 1 completion document consolidating evidence.

All three are now resolved in the repository.

## 8. Remaining Work After Phase 1

Phase 1 implementation is complete.

Pending work is Phase 2 only:

- Build Power BI pages and narratives for the 8 business questions.
- Add decision-oriented recommendations from the final visuals.

## 9. Reproducibility Notes

Run complete pipeline:

```bash
python src/run_pipeline.py
```

Expected success artifacts:

- `outputs/processed/integration_report.csv`
- `outputs/processed/powerbi_sales_trend_monthly.csv`
- `outputs/processed/powerbi_sales_by_region.csv`
- `outputs/processed/powerbi_product_performance.csv`
- `outputs/processed/powerbi_low_performance_regions.csv`
- `outputs/processed/powerbi_customer_value.csv`
- `outputs/processed/powerbi_geo_behavior.csv`
