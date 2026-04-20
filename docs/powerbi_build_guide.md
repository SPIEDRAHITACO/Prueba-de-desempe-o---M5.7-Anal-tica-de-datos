# Power BI Build Guide

## Data connection options

Option A (recommended): PostgreSQL direct connection.

- Connect to the PostgreSQL database.
- Import these views:
  - vw_sales_trend_monthly
  - vw_sales_by_region
  - vw_product_performance
  - vw_low_performance_regions
  - vw_customer_value
  - vw_geo_behavior

Option B: CSV import from `outputs/processed/powerbi_*.csv`.

## Suggested report pages

## Page 1: Executive Overview

Visuals:

- KPI: Total Sales
- KPI: Total Orders
- KPI: Average Sale per line
- Line chart: Monthly sales trend
- Map: Sales by country

Filters:

- Date range
- Region
- Product category

## Page 2: Product and Region Diagnosis

Visuals:

- Bar chart: Top products by sales
- Table: Bottom regions (low performance)
- Stacked bar: Sales by region and category

## Page 3: Customer Value Analysis

Visuals:

- Bar chart: Revenue by value segment
- Table: Top customers by revenue
- Scatter: frequency vs average ticket

## Page 4: Decision Actions

Visuals / elements:

- Card with key findings
- Prioritized action list
- Supporting numbers from previous pages

## Mandatory mapping to business questions

Ensure each question has at least one visual:

1. Sales evolution over time -> monthly trend chart.
2. Countries/regions with highest revenue -> map + region ranking.
3. Best-performing products -> product ranking chart.
4. Low-performing regions -> low region table.
5. Low-impact products -> bottom product ranking.
6. Highest-value customers -> value segment chart.
7. Geo-behavior relationship -> region behavior chart.
8. Recommended actions -> decision page.

## Presentation tips

- Keep titles action-oriented.
- Use one color palette consistently.
- Avoid clutter: prioritize 6-8 visuals per page max.
- Add short narrative text per page.
