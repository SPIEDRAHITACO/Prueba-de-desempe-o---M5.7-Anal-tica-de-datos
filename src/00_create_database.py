from __future__ import annotations

"""Create the target PostgreSQL database if it does not already exist."""

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from common import load_settings


def main() -> None:
    settings = load_settings()

    # Connect first to the default postgres database because the target database may not exist yet.
    connection_url_default = (
        f"postgresql+psycopg2://{settings['pg_user']}:{settings['pg_password']}"
        f"@{settings['pg_host']}:{settings['pg_port']}/postgres"
    )

    engine_default = create_engine(connection_url_default)

    try:
        with engine_default.connect() as conn:
            conn.execute(text("SELECT 1;"))
        print("[OK] Connected to PostgreSQL server.")
    except SQLAlchemyError as exc:
        raise RuntimeError(
            f"Connection to PostgreSQL failed: {exc}. "
            "Check .env credentials."
        ) from exc

    try:
        with engine_default.raw_connection() as raw_conn:
            # CREATE DATABASE must run outside a transaction block in PostgreSQL.
            raw_conn.driver_connection.autocommit = True
            cursor = raw_conn.cursor()
            cursor.execute(f"CREATE DATABASE {settings['pg_database']};")
            cursor.close()
        print(f"[OK] Database '{settings['pg_database']}' created successfully.")
    except Exception as exc:
        if "already exists" in str(exc):
            print(f"[INFO] Database '{settings['pg_database']}' already exists.")
        else:
            raise RuntimeError(f"Failed to create database: {exc}") from exc


if __name__ == "__main__":
    main()
