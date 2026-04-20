<!-- Practical guide for turning the prepared data into a Power BI report. -->

# Power BI Build Guide

## Phase 2 Goal

Build a clean Power BI report on top of the prepared PostgreSQL model or the exported CSV views.
This guide is ordered so each step can be completed without creating a blocker for the next one.

## Start Here

Use this order:

1. Choose one connection method.
2. Import the prepared analytical dataset.
3. Build the report pages in the suggested order.
4. Add visuals and filters.
5. Add short narrative text for each page.
6. Review the business-question mapping.

If you want the lowest-risk path, start with the CSV files in `outputs/processed/`.
If you want the more direct path, connect to PostgreSQL and use the `vw_*` views.

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

## Step 1: Connect the data

Pick one option and finish it completely before moving on.

### If you choose PostgreSQL

1. Open Power BI Desktop.
2. Select Get Data.
3. Choose PostgreSQL database.
4. Enter the server and database details.
5. Load the six views listed above.
6. Confirm that each view appears in the Fields pane.

### If you choose CSV files

1. Open Power BI Desktop.
2. Select Get Data.
3. Choose Text/CSV.
4. Import each file from `outputs/processed/` that starts with `powerbi_`.
5. Confirm that each table loads successfully.

## Suggested report pages

Build the pages in this order so the story flows from overview to decision.

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

Purpose:

- Give the business a fast view of overall performance and trend direction.

## Page 2: Product and Region Diagnosis

Visuals:

- Bar chart: Top products by sales
- Table: Bottom regions (low performance)
- Stacked bar: Sales by region and category

Purpose:

- Show where revenue comes from and where performance needs attention.

## Page 3: Customer Value Analysis

Visuals:

- Bar chart: Revenue by value segment
- Table: Top customers by revenue
- Scatter: frequency vs average ticket

Purpose:

- Show which customers drive value and how buying behavior varies.

## Page 4: Decision Actions

Visuals / elements:

- Card with key findings
- Prioritized action list
- Supporting numbers from previous pages

Purpose:

- Translate the analysis into next-step business actions.

## Step 2: Build the model

After the data is loaded, verify the fields and relationships you need.

1. If using PostgreSQL views, the views already contain the main analytical grain.
2. If using CSV files, keep each CSV as its own table.
3. Make sure date, region, product, and customer fields are available for slicing.
4. Do not add unnecessary calculated tables yet.

## Step 3: Create the report pages

1. Create Page 1 first and place the KPI cards and line chart.
2. Add Page 2 for region and product diagnosis.
3. Add Page 3 for customer value analysis.
4. Add Page 4 for final recommendations.

## Step 4: Add filters and formatting

1. Add the date slicer first.
2. Add region and product category slicers next.
3. Use one consistent color palette across the report.
4. Keep titles short and action-oriented.
5. Add a short subtitle or narrative sentence to each page.

## Step 5: Validate the business mapping

Ensure each question has at least one visual:

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

## Step 6: Final review

Before presenting the report, check that:

- Every page has a clear purpose.
- No page is overloaded with visuals.
- All visuals respond correctly to slicers.
- The report tells a story from summary to action.

## Presentation tips

- Keep titles action-oriented.
- Use one color palette consistently.
- Avoid clutter: prioritize 6-8 visuals per page max.
- Add short narrative text per page.
