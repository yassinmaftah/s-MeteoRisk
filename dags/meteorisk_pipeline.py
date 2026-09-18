from airflow import DAG
import sys
sys.path.append('/opt/airflow/')
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from extraction.extract_bronze import x
from transformation.clean_silver import x2
from gold.insert_data import x3
default_args = {
    'owner': 'yassine',
    'depends_on_past': False,
    'start_date': datetime(2026, 9, 18), 
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    's_meteorisk_daily_update',
    default_args=default_args,
    description='Pipeline ETL complet pour s-MeteoRisk',
    schedule_interval='0 2 * * *',
    catchup=False,
    tags=['MeteoRisk', 'ETL'],
) as dag:

    
    extract_task = PythonOperator(
        task_id='extract_api_to_bronze',
        python_callable=x,
    )

    transform_task = PythonOperator(
        task_id='clean_and_feature_engineering_silver',
        python_callable=x2,
    )

    load_task = PythonOperator(
        task_id='load_gold_to_postgres',
        python_callable=x3,
    )

    extract_task >> transform_task >> load_task