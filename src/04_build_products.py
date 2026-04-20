from __future__ import annotations

"""Create the product dimension and enrich sales with product identifiers."""

import pandas as pd

from common import PROCESSED_DIR, ensure_directories


def main() -> None:
    ensure_directories()

    # Build the product dimension from the cleaned sales source so product IDs stay deterministic.
    sales_path = PROCESSED_DIR / "sales_cleaned.csv"
    sales = pd.read_csv(sales_path, parse_dates=["orderdate"])

    # Unique product codes become the grain of the dimension.
    products = (
        sales[["productcode", "productline"]]
        .drop_duplicates()
        .sort_values(by=["productcode"])
        .reset_index(drop=True)
    )
    products["producto_id"] = products.index + 1
    products = products.rename(
        columns={
            "productcode": "producto_nombre",
            "productline": "categoria",
        }
    )

    products_output = PROCESSED_DIR / "products.csv"
    products.to_csv(products_output, index=False)

    # Enrich the sales fact source with product IDs so the database load can enforce keys.
    sales_with_product = sales.merge(
        products[["producto_id", "producto_nombre"]],
        left_on="productcode",
        right_on="producto_nombre",
        how="left",
    ).drop(columns=["producto_nombre"])

    sales_with_product_output = PROCESSED_DIR / "sales_with_product_id.csv"
    sales_with_product.to_csv(sales_with_product_output, index=False)

    print(f"[OK] Products dataset saved to: {products_output}")
    print(f"[OK] Sales with product_id saved to: {sales_with_product_output}")


if __name__ == "__main__":
    main()
