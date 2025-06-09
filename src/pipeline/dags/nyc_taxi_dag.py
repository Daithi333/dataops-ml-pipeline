from datetime import datetime, timedelta

from docker.types.services import Mount

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator

from config import Config
from etl import load_dataset

default_args = {
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    "load_and_transform_nyc_taxi",
    default_args=default_args,
    description="Load NYC taxi data into Postgres and run dbt on it",
    schedule=timedelta(days=1),
    start_date=datetime(2025, 6, 1),
    catchup=False,
    tags={"nyc_taxi"},
) as dag:

    load_task = PythonOperator(
        task_id="load_nyc_taxi_data",
        python_callable=load_dataset,
        op_kwargs={"dataset": "nyc_taxi"},
        execution_timeout=timedelta(minutes=60)
    )

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

    load_task >> dbt_run_task
