from airflow.decorators import dag
from airflow.models.variable import Variable
from pendulum import datetime
from etl_pipeline.tasks.staging.main import staging

@dag(
    dag_id = 'etl_pipeline',
    description = 'ETL pipeline for extracting data from Dellstore database, API, and spreadsheet into staging area.',
    start_date = datetime(2024, 9, 1),
    schedule = "@daily",
    catchup = False
)

def etl_pipeline():
    incremental_mode = eval(Variable.get('etl_pipeline_incremental_mode'))
    
    staging(incremental = incremental_mode)

etl_pipeline()