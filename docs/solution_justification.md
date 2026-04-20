<!-- Technical rationale for the solution architecture, modeling choices, and validation strategy. -->

# Solution Justification

## Problem Assessment

The challenge requires integrating heterogeneous sources (CSV + APIs), resolving data inconsistencies,
defining relationships not explicitly present in the data, and delivering decision-oriented analytics.

Main technical constraints detected:

- Sales data has no native customer key.
- Country names differ across sources.
- Dataset quality issues (missing fields, mixed formats, categorical consistency).
- Mandatory relational integration for products and customers.

## Why this approach

A pragmatic layered approach was selected to maximize score under time constraints:

1. Modular scripts with single responsibility.
2. Reproducible pipeline with deterministic behavior.
3. PostgreSQL relational model to enforce integrity.
4. SQL analytical views directly aligned with business questions.
5. Power BI-ready outputs for fast storytelling.

## Key technical decisions

### 1) Hybrid customer assignment

Since sales has no explicit customer ID, assignment strategy was defined as:

- Country-based mapping when possible.
- Seeded random fallback when country has no matching generated customers.

Rationale:

- Preserves geographic coherence.
- Guarantees full assignment coverage.
- Deterministic due to fixed random seed.

### 2) Product dimension from sales

Products are generated from unique product codes with numeric `producto_id`.
This satisfies the mandatory relationship `ventas.producto_id -> productos.producto_id`.

### 3) Country normalization

Normalization was applied before joins to reduce key fragmentation caused by naming variants.
This increases relationship coverage for geography enrichment.

### 4) PostgreSQL as integration core

PostgreSQL was chosen to:

- Materialize dimensions and fact table.
- Enforce key consistency through constraints.
- Provide stable views for dashboard consumption.

### 5) SQL views for analytical questions

Views were implemented to map directly to evaluation questions and reduce complexity in Power BI.

## Performance and efficiency choices

- Use vectorized operations in pandas for transformations.
- Keep data model compact (star-like structure) for fast BI queries.
- Push aggregated analysis to SQL views, minimizing repetitive dashboard calculations.

## Quality and validation strategy

Validation focuses on:

- Type parsing and critical null rates.
- Duplicate detection.
- Sales arithmetic consistency checks.
- Foreign key relation coverage.
- Country-match rate vs fallback rate in customer assignment.

## Risks and mitigations

- Synthetic customer assignment may not reflect real behavior.
  - Mitigation: explicitly documented assumption and deterministic logic.
- API country naming differences can reduce enrichment coverage.
  - Mitigation: normalization aliases and coverage tracking.
- Timebox limits advanced modeling depth.
  - Mitigation: prioritize complete, auditable, decision-ready baseline.

## How this exceeds baseline expectations

- Includes both relational integration and analytical layer.
- Delivers traceable assumptions and reproducibility.
- Produces both direct DB views and flat exports for BI flexibility.
- Connects technical outputs explicitly to business decision questions.
