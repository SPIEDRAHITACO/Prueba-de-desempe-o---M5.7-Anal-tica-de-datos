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

1. Ingest and profile sales data.
2. Build customer dimension from API.
3. Build geography dimension from API.
4. Build product dimension from sales.
5. Integrate all sources and load PostgreSQL model.
6. Create analytical SQL views.
7. Export view outputs for Power BI (optional if using direct DB connection).

### 4.2 Data Model

Relational structure in PostgreSQL:

- `dim_productos`
- `dim_clientes`
- `dim_paises`
- `fact_ventas`

Relationships:

- `fact_ventas.producto_id -> dim_productos.producto_id`
- `fact_ventas.cliente_id -> dim_clientes.cliente_id`
- `fact_ventas.country_normalized -> dim_paises.pais_normalizado`

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

1. Create a database (example: `emausoft_analytics`).
2. Copy `.env.example` to `.env` and update credentials.

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

## 12. Limitations and Improvement Opportunities

- Customer assignment is synthetic because source sales lacks direct customer IDs.
- No predictive ML was added due to pragmatic scope.
- For production, add CI/CD, orchestrator, and data quality gates.

## 13. Evaluation Alignment

This solution aligns with the requested criteria by providing:

- Organized modular code with clear responsibilities.
- Full integration of file and API sources.
- Efficient transformations with reproducibility.
- Justified technical decisions and explicit assumptions.
- Complete documentation for execution, logic, and business interpretation.