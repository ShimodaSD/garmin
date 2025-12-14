from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
from utils.test import init_process

with DAG(
    dag_id='daily_docker_job',
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:
    run_docker_task = PythonOperator(
        task_id='run_my_container',
        python_callable=init_process
    )
