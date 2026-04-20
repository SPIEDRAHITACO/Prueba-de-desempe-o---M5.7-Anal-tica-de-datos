from __future__ import annotations

"""Build the customer dimension from the RandomUser API."""

import requests
import pandas as pd

from common import PROCESSED_DIR, ensure_directories, normalize_country

RANDOMUSER_URL = "https://randomuser.me/api/?results=100&nat=us,gb,fr,es,de,au,ca,nl,se,no,dk,fi"


def main() -> None:
    ensure_directories()

    # This API provides realistic but synthetic customer identities for the fact table.
    response = requests.get(RANDOMUSER_URL, timeout=30)
    response.raise_for_status()
    payload = response.json()

    rows = []
    for idx, user in enumerate(payload.get("results", []), start=1):
        # Keep the customer structure simple and stable for relational loading.
        first = user.get("name", {}).get("first", "")
        last = user.get("name", {}).get("last", "")
        city = user.get("location", {}).get("city", "")
        country = user.get("location", {}).get("country", "")
        rows.append(
            {
                "cliente_id": idx,
                "nombre": f"{first} {last}".strip(),
                "ciudad": city,
                "pais": country,
                "pais_normalizado": normalize_country(country),
            }
        )

    customers = pd.DataFrame(rows)
    # Store the output as a dimension table source for the integration step.
    output = PROCESSED_DIR / "customers.csv"
    customers.to_csv(output, index=False)

    print(f"[OK] Customers dataset saved to: {output}")
    print(f"[INFO] Rows: {len(customers)}")


if __name__ == "__main__":
    main()
