from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from common import PROCESSED_DIR, SQL_DIR, ensure_directories, load_settings, normalize_country


def _build_connection_url(settings: dict) -> str:
    return (
        f"postgresql+psycopg2://{settings['pg_user']}:{settings['pg_password']}"
        f"@{settings['pg_host']}:{settings['pg_port']}/{settings['pg_database']}"
    )


def _assign_customers_hybrid(
    sales: pd.DataFrame,
    customers: pd.DataFrame,
    seed: int,
) -> tuple[pd.Series, float]:
    rng = np.random.default_rng(seed)

    country_to_customers = (
        customers.groupby("pais_normalizado")["cliente_id"].apply(list).to_dict()
    )
    all_customers = customers["cliente_id"].tolist()

    assigned = []
    matched_by_country = 0

    for country_norm in sales["country_normalized"]:
        candidates = country_to_customers.get(country_norm, [])
        if candidates:
            matched_by_country += 1
            assigned.append(int(rng.choice(candidates)))
        else:
            assigned.append(int(rng.choice(all_customers)))

    match_rate = matched_by_country / len(sales) if len(sales) > 0 else 0.0
    return pd.Series(assigned, name="cliente_id"), match_rate


def _execute_sql_file(engine, sql_file: Path) -> None:
    sql_text = sql_file.read_text(encoding="utf-8")
    with engine.begin() as conn:
        conn.execute(text(sql_text))


def main() -> None:
    ensure_directories()
    settings = load_settings()

    sales = pd.read_csv(PROCESSED_DIR / "sales_with_product_id.csv", parse_dates=["orderdate"])
    products = pd.read_csv(PROCESSED_DIR / "products.csv")
    customers = pd.read_csv(PROCESSED_DIR / "customers.csv")
    regions = pd.read_csv(PROCESSED_DIR / "regions.csv")

    sales["country_normalized"] = sales["country_normalized"].map(normalize_country)
    customers["pais_normalizado"] = customers["pais_normalizado"].map(normalize_country)
    regions["pais_normalizado"] = regions["pais_normalizado"].map(normalize_country)

    assigned_customer_ids, match_rate = _assign_customers_hybrid(
        sales=sales,
        customers=customers,
        seed=settings["seed"],
    )
    sales["cliente_id"] = assigned_customer_ids

    sales["venta_linea_id"] = np.arange(1, len(sales) + 1)

    fact_columns = [
        "venta_linea_id",
        "ordernumber",
        "orderlinenumber",
        "orderdate",
        "status",
        "quantityordered",
        "priceeach",
        "sales",
        "qtr_id",
        "month_id",
        "year_id",
        "territory",
        "dealsize",
        "country",
        "country_normalized",
        "producto_id",
        "cliente_id",
    ]
    fact_sales = sales[fact_columns].copy()

    dim_paises = (
        regions[
            [
                "pais_normalizado",
                "pais_oficial",
                "continente",
                "region",
                "subregion",
                "latitude",
                "longitude",
                "cca2",
                "cca3",
            ]
        ]
        .drop_duplicates(subset=["pais_normalizado"])
        .reset_index(drop=True)
    )

    connection_url = _build_connection_url(settings)
    engine = create_engine(connection_url)

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
    except SQLAlchemyError as exc:
        raise RuntimeError(
            "PostgreSQL connection failed. Check .env values for PG_HOST, PG_PORT, "
            "PG_DATABASE, PG_USER, and PG_PASSWORD."
        ) from exc

    _execute_sql_file(engine, SQL_DIR / "schema.sql")

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE fact_ventas RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_productos RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_clientes RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_paises RESTART IDENTITY CASCADE;"))

    products.to_sql("dim_productos", engine, if_exists="append", index=False)
    customers.to_sql("dim_clientes", engine, if_exists="append", index=False)
    dim_paises.to_sql("dim_paises", engine, if_exists="append", index=False)
    fact_sales.to_sql("fact_ventas", engine, if_exists="append", index=False)

    _execute_sql_file(engine, SQL_DIR / "analytics_views.sql")

    integration_report = pd.DataFrame(
        [
            {
                "rows_fact_ventas": len(fact_sales),
                "rows_dim_productos": len(products),
                "rows_dim_clientes": len(customers),
                "rows_dim_paises": len(dim_paises),
                "customer_match_rate_by_country": round(match_rate, 4),
                "fallback_rate": round(1.0 - match_rate, 4),
            }
        ]
    )
    report_path = PROCESSED_DIR / "integration_report.csv"
    integration_report.to_csv(report_path, index=False)

    print("[OK] PostgreSQL integration completed.")
    print(f"[OK] Integration report saved to: {report_path}")


if __name__ == "__main__":
    main()
