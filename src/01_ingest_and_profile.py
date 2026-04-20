from __future__ import annotations

import json

import pandas as pd

from common import DOCS_DIR, PROCESSED_DIR, REPORTS_DIR, ensure_directories, normalize_country


def main() -> None:
    ensure_directories()

    sales_path = DOCS_DIR / "sales_data_sample.csv"
    df = pd.read_csv(sales_path, encoding="latin1")
    df.columns = [c.strip().lower() for c in df.columns]

    df["orderdate"] = pd.to_datetime(df["orderdate"], errors="coerce")
    numeric_cols = ["quantityordered", "priceeach", "sales", "msrp"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ["status", "productline", "productcode", "country", "territory", "dealsize"]:
        df[col] = df[col].astype(str).str.strip()

    df["country_normalized"] = df["country"].map(normalize_country)

    duplicate_rows = int(df.duplicated().sum())
    nulls = df.isna().sum().to_dict()
    invalid_dates = int(df["orderdate"].isna().sum())

    expected_sales = (df["quantityordered"] * df["priceeach"]).round(2)
    sales_diff = (df["sales"] - expected_sales).abs()
    inconsistent_sales_rows = int((sales_diff > 0.05).sum())

    critical_columns = [
        "ordernumber",
        "orderdate",
        "productcode",
        "quantityordered",
        "priceeach",
        "sales",
        "country",
    ]

    quality_report = {
        "row_count": int(len(df)),
        "column_count": int(df.shape[1]),
        "duplicate_rows": duplicate_rows,
        "invalid_dates": invalid_dates,
        "inconsistent_sales_rows": inconsistent_sales_rows,
        "nulls_by_column": nulls,
        "critical_column_null_rate": {
            col: float(df[col].isna().mean()) for col in critical_columns
        },
        "status_domain": sorted(df["status"].dropna().unique().tolist()),
        "territory_domain": sorted(df["territory"].dropna().unique().tolist()),
        "dealsize_domain": sorted(df["dealsize"].dropna().unique().tolist()),
        "date_min": str(df["orderdate"].min()),
        "date_max": str(df["orderdate"].max()),
    }

    cleaned_path = PROCESSED_DIR / "sales_cleaned.csv"
    df.to_csv(cleaned_path, index=False)

    report_json_path = REPORTS_DIR / "data_quality_report.json"
    report_json_path.write_text(json.dumps(quality_report, indent=2), encoding="utf-8")

    report_md_path = REPORTS_DIR / "data_quality_report.md"
    report_md_path.write_text(
        "\n".join(
            [
                "# Data Quality Report",
                "",
                f"- Rows: {quality_report['row_count']}",
                f"- Columns: {quality_report['column_count']}",
                f"- Duplicate rows: {quality_report['duplicate_rows']}",
                f"- Invalid order dates: {quality_report['invalid_dates']}",
                f"- Inconsistent sales rows: {quality_report['inconsistent_sales_rows']}",
                f"- Date range: {quality_report['date_min']} to {quality_report['date_max']}",
                "",
                "## Domain Checks",
                f"- STATUS: {', '.join(quality_report['status_domain'])}",
                f"- TERRITORY: {', '.join(quality_report['territory_domain'])}",
                f"- DEALSIZE: {', '.join(quality_report['dealsize_domain'])}",
                "",
                "## Critical Null Rates",
            ]
            + [
                f"- {k}: {v:.2%}"
                for k, v in quality_report["critical_column_null_rate"].items()
            ]
        ),
        encoding="utf-8",
    )

    print(f"[OK] Cleaned sales saved to: {cleaned_path}")
    print(f"[OK] Quality report saved to: {report_json_path}")


if __name__ == "__main__":
    main()
