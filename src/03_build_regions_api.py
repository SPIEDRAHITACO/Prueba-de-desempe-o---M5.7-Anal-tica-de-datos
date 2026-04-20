from __future__ import annotations

"""Build the geography dimension from the RestCountries API."""

import requests
import pandas as pd

from common import PROCESSED_DIR, ensure_directories, normalize_country

RESTCOUNTRIES_URLS = [
    "https://restcountries.com/v3.1/all?fields=name,region,subregion,continents,latlng,cca2,cca3",
    "https://restcountries.com/v3.1/all",
]


def _fetch_countries() -> list[dict]:
    # Try a field-restricted endpoint first to reduce payload size, then fall back if needed.
    headers = {"User-Agent": "emausoft-analytics-pipeline/1.0"}
    last_error = None

    for url in RESTCOUNTRIES_URLS:
        try:
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            last_error = exc

    raise RuntimeError(f"Unable to fetch countries data from RestCountries API: {last_error}")


def main() -> None:
    ensure_directories()

    # Geography metadata enriches the sales facts with continent and region context.
    countries = _fetch_countries()

    rows = []
    for item in countries:
        # Normalize the country name so it can match the sales source consistently.
        name_common = item.get("name", {}).get("common", "")
        continents = item.get("continents") or []
        latlng = item.get("latlng") or [None, None]

        rows.append(
            {
                "pais_oficial": name_common,
                "pais_normalizado": normalize_country(name_common),
                "region": item.get("region", ""),
                "subregion": item.get("subregion", ""),
                "continente": continents[0] if continents else "",
                "latitude": latlng[0] if len(latlng) > 0 else None,
                "longitude": latlng[1] if len(latlng) > 1 else None,
                "cca2": item.get("cca2", ""),
                "cca3": item.get("cca3", ""),
            }
        )

    regions = pd.DataFrame(rows).drop_duplicates(subset=["pais_normalizado"]).reset_index(drop=True)
    # Save the deduplicated geography dimension source for downstream joins.
    output = PROCESSED_DIR / "regions.csv"
    regions.to_csv(output, index=False)

    print(f"[OK] Regions dataset saved to: {output}")
    print(f"[INFO] Rows: {len(regions)}")


if __name__ == "__main__":
    main()
