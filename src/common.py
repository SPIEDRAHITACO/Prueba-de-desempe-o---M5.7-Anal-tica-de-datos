from __future__ import annotations

import os
import unicodedata
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT_DIR / "docs"
OUTPUTS_DIR = ROOT_DIR / "outputs"
PROCESSED_DIR = OUTPUTS_DIR / "processed"
REPORTS_DIR = OUTPUTS_DIR / "reports"
SQL_DIR = ROOT_DIR / "sql"


COUNTRY_ALIASES = {
    "usa": "united states",
    "u.s.a": "united states",
    "us": "united states",
    "uk": "united kingdom",
    "u.k.": "united kingdom",
    "korea": "south korea",
    "republic of korea": "south korea",
    "russian federation": "russia",
    "viet nam": "vietnam",
    "czech republic": "czechia",
}


def ensure_directories() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def normalize_text(value: str) -> str:
    if value is None:
        return ""
    normalized = unicodedata.normalize("NFKD", str(value))
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.strip().lower().split())


def normalize_country(country: str) -> str:
    norm = normalize_text(country)
    return COUNTRY_ALIASES.get(norm, norm)


def load_settings() -> dict:
    load_dotenv(ROOT_DIR / ".env")
    return {
        "pg_host": os.getenv("PG_HOST", "localhost"),
        "pg_port": int(os.getenv("PG_PORT", "5432")),
        "pg_database": os.getenv("PG_DATABASE", "emausoft_analytics"),
        "pg_user": os.getenv("PG_USER", "postgres"),
        "pg_password": os.getenv("PG_PASSWORD", "postgres"),
        "seed": int(os.getenv("PIPELINE_RANDOM_SEED", "42")),
    }
