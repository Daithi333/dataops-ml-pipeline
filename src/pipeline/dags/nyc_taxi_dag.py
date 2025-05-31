from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

from etl import load_dataset

default_args = {
    "owner": "dataops",
    "depends_on_past": False,
    "start_date": datetime(2025, 5, 25),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    "load_and_transform_nyc_taxi",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    load_task = PythonOperator(
        task_id="load_nyc_taxi_data",
        python_callable=load_dataset,
        op_kwargs={"dataset": "nyc_taxi"},
        execution_timeout=timedelta(minutes=60)
    )

    dbt_run_task = BashOperator(
        task_id="dbt_run",
        bash_command="docker exec dataops_dbt dbt run --verbose",
    )

    load_task >> dbt_run_task
