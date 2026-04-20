from __future__ import annotations

"""Run the complete Phase 1 pipeline from database creation to Power BI exports."""

import subprocess
import sys
from pathlib import Path


SCRIPTS = [
    "00_create_database.py",
    "01_ingest_and_profile.py",
    "02_build_customers_api.py",
    "03_build_regions_api.py",
    "04_build_products.py",
    "05_integrate_and_load_pg.py",
    "06_export_powerbi_views.py",
]


def main() -> None:
    src_dir = Path(__file__).resolve().parent

    for script_name in SCRIPTS:
        # Run the pipeline in sequence because each step produces inputs for the next one.
        script_path = src_dir / script_name
        print(f"[RUN] {script_name}")
        subprocess.run([sys.executable, str(script_path)], check=True)

    print("[OK] Full pipeline completed.")


if __name__ == "__main__":
    main()
