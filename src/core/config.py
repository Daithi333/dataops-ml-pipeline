import os


class Config:

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PW = os.getenv("DB_PW", "postgres")
    ANALYTICS_DB_NAME = os.getenv("DB_NAME", "analytics")
    AIRFLOW_DB_NAME = os.getenv("DB_NAME", "airflow")

    ANALYTICS_DB_URL = f"postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{ANALYTICS_DB_NAME}"
    AIRFLOW_DB_URL = f"postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{AIRFLOW_DB_NAME}"

    DB_POOL_SIZE = int(os.environ.get("DB_POOL_SIZE", 20))
    DB_MAX_OVERFLOW = int(os.environ.get("DB_MAX_OVERFLOW", 20))

    DATASETS = {
        "nyc_taxi": ("datasets/nyc_taxi/raw/", "parquet", "yellow_taxi_data"),
    }
