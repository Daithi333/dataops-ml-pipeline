from core.etl.load_data import load_csv_files_to_postgres

load_csv_files_to_postgres(
    directory_path="datasets/nyc_taxi/raw/",
    file_type="parquet",
    table_name="yellow_taxi_data",
)
