import os
import glob
import pandas as pd
import pyarrow.parquet as pq
from datetime import datetime
from loguru import logger
from sqlalchemy import text
from typing import Literal

from sqlalchemy.engine.base import Connection

from core.database import db


def load_files_to_postgres(
    directory_path: str,
    file_type: Literal["csv", "parquet"],
    table_name: str,
    schema: str = "public",
    truncate_table: bool = False,
):
    """
    Load files of the given type from the given directory into a Postgres table,
    skipping those already loaded. Also creates a tracking table to record file loads.
    """

    engine = db.engine

    with engine.begin() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))

        conn.execute(
            text(f"""
            CREATE TABLE IF NOT EXISTS {schema}.file_load_log (
                file_name TEXT PRIMARY KEY,
                loaded_at TIMESTAMP
            );
        """)
        )

        if truncate_table:
            conn.execute(text(f"TRUNCATE TABLE {schema}.{table_name};"))
            conn.execute(text(f"TRUNCATE TABLE {schema}.file_load_log;"))

    files = glob.glob(f"{directory_path}/*.{file_type}")
    logger.info(f"Discovered {len(files)} {file_type} files to load...")

    for file_path in files:
        load_file_to_postgres(file_path, file_type, table_name, schema)

    logger.info("✅ All new files loaded.")


def list_eligible_files(
    directory_path: str, file_type: Literal["csv", "parquet"]
) -> list[str]:
    """List all the files of a given type in the directory"""
    files = glob.glob(f"{directory_path}/*.{file_type}")
    logger.info(
        f"Found {len(files)} {file_type} files in directory '{directory_path}' ..."
    )
    return files


def load_file_to_postgres(
    file_path: str,
    file_type: Literal["csv", "parquet"],
    table_name: str,
    schema: str = "public",
):
    """Load single file to Postgres table, skipping those already loaded."""
    engine = db.engine
    file_name = os.path.basename(file_path)

    # Check if file has already been loaded
    with engine.connect() as conn:
        result = conn.execute(
            text(f"SELECT 1 FROM {schema}.file_load_log WHERE file_name = :fname"),
            {"fname": file_name},
        ).fetchone()

    if result:
        logger.info(f"Skipping '{file_name}' (already loaded).")
        return

    logger.info(f"Loading '{file_name}' ...")
    with engine.begin() as conn:
        if file_type == "csv":
            _load_csv_in_chunks(conn, schema, table_name, file_path)
        elif file_type == "parquet":
            _load_parquet_in_chunks(conn, schema, table_name, file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        _record_file_completion(conn, schema, file_name)
        logger.info(f"File '{file_name}' load complete")


def _load_parquet_in_chunks(
    conn: Connection, schema: str, table_name: str, file_path: str
) -> None:
    parquet_file = pq.ParquetFile(file_path)
    num_row_groups = parquet_file.num_row_groups

    for i in range(num_row_groups):
        logger.debug(f"Processing row group {i + 1} / {num_row_groups}")
        table = parquet_file.read_row_group(i)
        df = table.to_pandas()
        df.to_sql(table_name, con=conn, schema=schema, if_exists="append", index=False)


def _load_csv_in_chunks(
    conn: Connection, schema: str, table_name: str, file_path: str, chunk_size=100_000
) -> None:
    chunk_iter = pd.read_csv(file_path, chunksize=chunk_size)

    for i, chunk in enumerate(chunk_iter):
        logger.debug(f"Processing chunk {i + 1}")
        chunk.to_sql(
            table_name, con=conn, schema=schema, if_exists="append", index=False
        )


def _record_file_completion(conn: Connection, schema: str, file_name: str):
    conn.execute(
        text(
            f"INSERT INTO {schema}.file_load_log (file_name, loaded_at) VALUES (:fname, :ts)"
        ),
        {"fname": file_name, "ts": datetime.utcnow()},
    )
