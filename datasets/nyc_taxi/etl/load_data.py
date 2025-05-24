from core.etl.load_data import load_files_to_postgres


def load_nyc_taxi_data():
    load_files_to_postgres(
        directory_path="datasets/nyc_taxi/raw/",
        file_type="parquet",
        table_name="yellow_taxi_data",
    )


if __name__ == "__main__":
    load_nyc_taxi_data()
