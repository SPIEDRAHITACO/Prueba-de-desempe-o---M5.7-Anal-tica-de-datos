from __future__ import annotations

"""Export PostgreSQL analytical views to CSV files for Power BI consumption."""

import pandas as pd
from sqlalchemy import create_engine

from common import PROCESSED_DIR, ensure_directories, load_settings


VIEWS_TO_EXPORT = {
    "vw_sales_trend_monthly": "powerbi_sales_trend_monthly.csv",
    "vw_sales_by_region": "powerbi_sales_by_region.csv",
    "vw_product_performance": "powerbi_product_performance.csv",
    "vw_low_performance_regions": "powerbi_low_performance_regions.csv",
    "vw_customer_value": "powerbi_customer_value.csv",
    "vw_geo_behavior": "powerbi_geo_behavior.csv",
}


def _build_connection_url(settings: dict) -> str:
    return (
        f"postgresql+psycopg2://{settings['pg_user']}:{settings['pg_password']}"
        f"@{settings['pg_host']}:{settings['pg_port']}/{settings['pg_database']}"
    )


def main() -> None:
    ensure_directories()
    settings = load_settings()
    engine = create_engine(_build_connection_url(settings))

    for view_name, output_name in VIEWS_TO_EXPORT.items():
        # Export each reporting view to a flat file so Power BI can use it without SQL access.
        query = f"SELECT * FROM {view_name};"
        frame = pd.read_sql(query, engine)
        output_path = PROCESSED_DIR / output_name
        frame.to_csv(output_path, index=False)
        print(f"[OK] Exported {view_name} to: {output_path}")


if __name__ == "__main__":
    main()
