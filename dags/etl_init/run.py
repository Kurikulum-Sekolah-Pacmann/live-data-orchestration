from airflow.decorators import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from pendulum import datetime
from helper.minio import MinioClient

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
        task_id = 'init_stg_schema',
        conn_id = 'staging_db',
        sql = 'models/staging.sql'
    )

    create_bucket() >> init_stg_schema

etl_init()