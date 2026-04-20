<!-- General project overview. This file explains the solution at a high level and points to the execution and reporting artifacts. -->

# Emausoft End-to-End Analytics Solution

## 1. Project Goal

This project delivers an end-to-end analytical solution for Emausoft.
It integrates transactional sales data with API-generated customers and country metadata,
builds a relational model in PostgreSQL, and prepares analytical outputs for Power BI.

The implementation is designed for:

- Clear and maintainable code.
- Reproducible data processing.
- Business-oriented analysis and storytelling.
- Fast execution within an evaluation timebox.

## 2. Business Questions Covered

The analytical layer and dashboard support these questions:

1. How have sales evolved over time?
2. Which countries or regions generate the most revenue?
3. Which products perform best?
4. Which regions show low performance?
5. Which products have lower impact on sales?
6. What type of customers generate higher value?
7. Is there a relationship between location and purchase behavior?
8. What actions should the business prioritize based on the data?

## 3. Data Sources

- Sales dataset: `docs/sales_data_sample.csv`
- Customers API: `https://randomuser.me/api/?results=100`
- Regions API: `https://restcountries.com/v3.1/all`

## 4. Solution Architecture

### 4.1 Processing Flow

1. Create PostgreSQL database (idempotent).
2. Ingest and profile sales data.
3. Build customer dimension from API.
4. Build geography dimension from API.
5. Build product dimension from sales.
6. Integrate all sources and load PostgreSQL star schema.
7. Create analytical SQL views.
8. Export view outputs for Power BI (optional if using direct DB connection).

### 4.2 Data Model

Relational structure in PostgreSQL:

- `dim_fecha`
- `dim_geografia`
- `dim_productos`
- `dim_clientes`
- `fact_ventas`

Relationships:

- `fact_ventas.fecha_id -> dim_fecha.fecha_id`
- `fact_ventas.geografia_id -> dim_geografia.geografia_id`
- `fact_ventas.producto_id -> dim_productos.producto_id`
- `fact_ventas.cliente_id -> dim_clientes.cliente_id`

## 5. Repository Structure

```text
.
├── docs/
│   └── sales_data_sample.csv
├── outputs/
│   ├── processed/
│   └── reports/
├── sql/
│   ├── schema.sql
│   └── analytics_views.sql
├── src/
│   ├── 00_create_database.py
│   ├── common.py
│   ├── 01_ingest_and_profile.py
│   ├── 02_build_customers_api.py
│   ├── 03_build_regions_api.py
│   ├── 04_build_products.py
│   ├── 05_integrate_and_load_pg.py
│   ├── 06_export_powerbi_views.py
│   └── run_pipeline.py
├── .env.example
├── requirements.txt
└── README.md
```

## 6. Setup Instructions

### 6.1 Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 6.2 PostgreSQL environment

1. Copy `.env.example` to `.env` and update credentials.
2. The pipeline creates the target database automatically if it does not exist.

Example:

```bash
cp .env.example .env
```

## 7. Pipeline Execution

Run the complete pipeline:

```bash
python src/run_pipeline.py
```

Or run step-by-step:

```bash
python src/00_create_database.py
python src/01_ingest_and_profile.py
python src/02_build_customers_api.py
python src/03_build_regions_api.py
python src/04_build_products.py
python src/05_integrate_and_load_pg.py
python src/06_export_powerbi_views.py
```

## 8. Core Design Decisions

### 8.1 Customer assignment logic (required by challenge)

Because sales data has no explicit customer ID, this solution uses a hybrid assignment:

- First attempt: assign a customer from the same normalized country.
- Fallback: seeded random assignment from all customers.

This ensures full coverage while preserving geographic coherence when possible.

### 8.2 Country normalization

Country names are normalized to support robust joins across datasets
(examples: `USA -> united states`, `UK -> united kingdom`).

### 8.3 Product dimension construction

Products are generated from unique `PRODUCTCODE` values in sales.
Each product receives a deterministic numeric `producto_id`.

## 9. Outputs

### 9.1 Processed outputs

- `outputs/processed/sales_cleaned.csv`
- `outputs/processed/customers.csv`
- `outputs/processed/regions.csv`
- `outputs/processed/products.csv`
- `outputs/processed/sales_with_product_id.csv`
- `outputs/processed/integration_report.csv`
- `outputs/processed/powerbi_*.csv`

### 9.2 Quality reports

- `outputs/reports/data_quality_report.json`
- `outputs/reports/data_quality_report.md`

## 10. Power BI Integration

Two options:

1. Connect directly to PostgreSQL and consume `vw_*` views.
2. Use exported CSV files from `outputs/processed/powerbi_*.csv`.

Recommended visuals:

- KPI cards (total sales, total orders, avg sale).
- Sales trend by month.
- Sales by country/region map.
- Product performance ranking.
- Low-performance region table.
- Customer value segmentation chart.

## 11. Validation Checklist

- Critical columns parsed correctly.
- Duplicate and null analysis generated.
- Product and customer keys assigned to all fact rows.
- PostgreSQL foreign keys respected.
- All required business questions mapped to views/visuals.

## 12. Phase 1 Completion Status

Phase 1 is complete in this repository.

Evidence generated by the latest successful run:

- `outputs/processed/integration_report.csv`
  - `rows_fact_ventas`: 2823
  - `rows_dim_fecha`: 252
  - `rows_dim_geografia`: 250
  - `rows_dim_productos`: 109
  - `rows_dim_clientes`: 100
  - `customer_match_rate_by_country`: 0.853
  - `fallback_rate`: 0.147
- `outputs/reports/data_quality_report.md`
- `outputs/processed/powerbi_*.csv`

Note: customer match rates can vary between executions because customer records are generated from a live API.

## 13. Limitations and Improvement Opportunities

- Customer assignment is synthetic because source sales lacks direct customer IDs.
- No predictive ML was added due to pragmatic scope.
- For production, add CI/CD, orchestrator, and data quality gates.

## 14. File Guide

For a general-purpose explanation of every important file and folder in the repository, see [docs/FILE_GUIDE_ES.md](docs/FILE_GUIDE_ES.md).

## 15. Evaluation Alignment

This solution aligns with the requested criteria by providing:

- Organized modular code with clear responsibilities.
- Full integration of file and API sources.
- Efficient transformations with reproducibility.
- Justified technical decisions and explicit assumptions.
- Complete documentation for execution, logic, and business interpretation.