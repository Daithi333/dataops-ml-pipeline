from datetime import timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

from dbt.etl import list_dataset_files, load_dataset_file

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
}

with DAG(
    "load_and_transform_nyc_taxi_alt",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:
    """Alternative where each file gets it own task, due to DAG processing timeout (zombie job status)"""

    @task
    def list_files():
        return list_dataset_files(dataset="nyc_taxi")

    @task(execution_timeout=timedelta(minutes=15))
    def load_file(file_path: str):
        load_dataset_file(dataset="nyc_taxi", file_path=file_path)

    file_paths = list_files()
    load_tasks = load_file.expand(file_path=file_paths)

    dbt_task = BashOperator(
        task_id="run_dbt",
        bash_command="docker exec dataops_dbt dbt run",
    )

    # Chain: all file loads must finish before dbt runs
    load_tasks >> dbt_task
