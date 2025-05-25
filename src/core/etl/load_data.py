import os
import glob
import pandas as pd
from datetime import datetime
from loguru import logger
from sqlalchemy import text, MetaData
from typing import Literal

from core.database import analytics_db


def load_files_to_postgres(
    directory_path: str,
    file_type: Literal["csv", "parquet"],
    table_name: str,
    schema: str = "public",
    if_exists: Literal["fail", "replace", "append"] = "append",
    truncate_table: bool = False,
):
    """
    Load files of the given type from the given directory into a Postgres table,
    skipping those already loaded. Also creates a tracking table to record file loads.
    """

    engine = analytics_db.engine
    metadata = MetaData()

    # Create schema and tracking table
    with engine.begin() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))

        # Create tracking table if not exists
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS {schema}.file_load_log (
                file_name TEXT PRIMARY KEY,
                loaded_at TIMESTAMP
            );
        """))

        if truncate_table:
            conn.execute(text(f"TRUNCATE TABLE {schema}.{table_name};"))
            conn.execute(text(f"TRUNCATE TABLE {schema}.file_load_log;"))

    # Discover files
    files = glob.glob(f"{directory_path}/*.{file_type}")
    logger.info(f"Discovered {len(files)} {file_type} files to load...")

    # Load files
    for file_path in files:
        file_name = os.path.basename(file_path)

        # Check if file has already been loaded
        with engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT 1 FROM {schema}.file_load_log WHERE file_name = :fname"),
                {"fname": file_name}
            ).fetchone()

        if result:
            logger.info(f"Skipping '{file_name}' (already loaded).")
            continue

        # Load the file
        logger.info(f"Loading '{file_name}' ...")
        if file_type == 'csv':
            df = pd.read_csv(file_path)
        elif file_type == 'parquet':
            df = pd.read_parquet(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        # Write to database
        with engine.begin() as conn:
            df.to_sql(table_name, con=conn, schema=schema, if_exists=if_exists, index=False)

            # Record file load
            conn.execute(
                text(f"INSERT INTO {schema}.file_load_log (file_name, loaded_at) VALUES (:fname, :ts)"),
                {"fname": file_name, "ts": datetime.utcnow()}
            )

    logger.info("✅ All new files loaded.")
