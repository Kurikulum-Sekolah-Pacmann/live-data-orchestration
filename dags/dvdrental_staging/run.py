from airflow.decorators import dag
from pendulum import datetime

from dvdrental_staging.tasks.main import extract, load
from helper.callbacks.slack_notifier import slack_notifier
from airflow.models.variable import Variable

default_args = {
    'on_failure_callback': slack_notifier
}

@dag(
    dag_id='dvdrental_staging',
    description='Extract data and load into staging area',
    start_date=datetime(2024, 9, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args
)

def dvdrental_staging():
    incremental_mode = eval(Variable.get('dvdrental_staging_incremental_mode'))

    extract(incremental=incremental_mode) >> load(incremental=incremental_mode)

dvdrental_staging()