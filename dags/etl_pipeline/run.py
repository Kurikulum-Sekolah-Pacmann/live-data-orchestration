from airflow.decorators import dag, task_group
from pendulum import datetime

from etl_pipeline.tasks.staging.dellstore_db import dellstore_db
from etl_pipeline.tasks.staging.dellstore_api import dellstore_api
from etl_pipeline.tasks.staging.dellstore_spreadsheet import dellstore_spreadsheet

@dag(
    dag_id = 'etl_pipeline',
    description = 'ETL pipeline for extracting data from Dellstore database, API, and spreadsheet into staging area.',
    start_date = datetime(2024, 9, 1),
    schedule = "@daily",
    catchup = False
)

def etl_pipeline():
    @task_group
    def staging():  
        dellstore_db(incremental = True) >> dellstore_api() >> dellstore_spreadsheet() 

    staging()

etl_pipeline()