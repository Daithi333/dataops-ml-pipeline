from datetime import timedelta, datetime

from docker.types import Mount

from airflow import DAG
from airflow.decorators import task
from airflow.providers.docker.operators.docker import DockerOperator

from config import Config
from etl import list_dataset_files, load_dataset_file

default_args = {
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "load_and_transform_nyc_taxi_alt",
    default_args=default_args,
    description="Load NYC taxi data into Postgres and run dbt on it",
    schedule=timedelta(days=1),
    start_date=datetime(2025, 6, 1),
    catchup=False,
    tags={"nyc_taxi"},
) as dag:
    """Alternative DAG where each file gets it own task, due to DAG processing timeout"""

    @task
    def list_files():
        return list_dataset_files(dataset="nyc_taxi")

    @task(execution_timeout=timedelta(minutes=15), max_active_tis_per_dag=2)
    def load_file(file_path: str):
        load_dataset_file(dataset="nyc_taxi", file_path=file_path)

    file_paths = list_files()
    load_tasks = load_file.expand(file_path=file_paths)

    dbt_run_task = DockerOperator(
        task_id="run_dbt",
        image="ghcr.io/dbt-labs/dbt-postgres",
        command="dbt run --project-dir /dbt/nyc_taxi --profiles-dir /dbt",
        network_mode="bridge",
        mounts=[
            Mount(source='dbt_project', target='/dbt', type='volume'),
            Mount(source='datasets', target='/datasets', type='volume'),
        ],
        auto_remove="success",
        docker_url=Config.DOCKER_URL,
        api_version="auto",
    )

    load_tasks >> dbt_run_task
