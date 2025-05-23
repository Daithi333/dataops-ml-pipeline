import glob
from typing import Literal

import pandas as pd
from loguru import logger
from sqlalchemy import text
from core.database import db


def load_csv_files_to_postgres(
    directory_path: str,
    file_type: Literal["csv", "parquet"],
    table_name: str,
    schema: str = "public",
    if_exists: Literal["fail", "replace", "append"] = "append",
    truncate_table: bool = False,
):
    """
    Load a files of the given type from the given directory into a Postgres table.

    Parameters:
    - directory_path (str): Path to the directory containing the files.
    - file_type (str): The type of the files.
    - table_name (str): Destination table name.
    - schema (str): Postgres schema name.
    - if_exists (str): One of 'fail', 'replace', 'append'.
    """

    with db.engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
        if truncate_table:
            conn.execute(text(f"TRUNCATE TABLE {schema}.{table_name};"))

    files = glob.glob(f"{directory_path}/*.{file_type}")

    for file in files:
        logger.info(f"Loading '{file}' ...")
        if file_type == 'csv':
            df = pd.read_csv(file)
            df.to_sql(table_name, db.engine, schema=schema, if_exists=if_exists, index=False)
        elif file_type == 'parquet':
            df = pd.read_parquet(file)
            df.to_sql(table_name, db.engine, schema=schema, if_exists=if_exists, index=False)
        else:
            raise ValueError(f"File type '{file_type}' unsupported")

    logger.info("All files loaded.")
