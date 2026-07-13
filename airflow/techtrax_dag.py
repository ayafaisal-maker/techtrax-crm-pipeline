from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "aya",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="techtrax_crm_pipeline",
    default_args=default_args,
    description="Extract TechTrax CRM data from MongoDB and load into BigQuery",
    schedule_interval="@daily",  # يشتغل يوميًا - تقدري تغيريها لـ "0 */6 * * *" لكل 6 ساعات مثلاً
    start_date=datetime(2026, 7, 1),
    catchup=False,
    tags=["techtrax", "crm", "etl"],
) as dag:

    extract = BashOperator(
        task_id="extract_from_mongodb",
        bash_command="cd /path/to/techtrax-pipeline/src && python extract.py",
    )

    convert = BashOperator(
        task_id="convert_to_ndjson",
        bash_command="cd /path/to/techtrax-pipeline/src && python convert_to_ndjson.py",
    )

    upload = BashOperator(
        task_id="upload_to_gcs",
        bash_command="cd /path/to/techtrax-pipeline/src && python upload_to_gcs.py",
    )

    load = BashOperator(
        task_id="load_to_bigquery",
        bash_command="cd /path/to/techtrax-pipeline/src && python load_to_bigquery.py",
    )

    extract >> convert >> upload >> load