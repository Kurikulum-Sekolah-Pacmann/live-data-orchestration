from airflow.decorators import dag, task, task_group
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from pendulum import datetime
from helper.minio import MinioClient
from etl_pipeline.tasks.staging.dellstore_db import dellstore_db

@dag(
    dag_id = 'etl_init',
    start_date = datetime(2024, 9, 1),
    schedule = "@once",
    catchup = False
)

def etl_init():
    @task
    def create_bucket():
        minio_client = MinioClient._get()
        bucket_name = 'extracted-data'
        
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)

    init_stg_schema = SQLExecuteQueryOperator(
        task_id='init_stg_schema',
        conn_id="staging_db",
        sql="models/staging.sql"
    )

    @task_group
    def init_load_stg():
        dellstore_db(incremental = False)

    create_bucket() >> init_stg_schema >> init_load_stg()

etl_init()