from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.exceptions import AirflowSkipException
from airflow import AirflowException

from helper.minio import CustomMinio
from sqlalchemy import create_engine
from pangres import upsert
from datetime import timedelta

import pandas as pd

class Load:
    @staticmethod
    def _dvdrental(table_name, incremental, **kwargs):
        try:
            date = kwargs.get('ds')
            table_pkey = kwargs.get('table_pkey')

            object_name = f'/dvdrental/{table_name}-{(pd.to_datetime(date) - timedelta(days=1)).strftime("%Y-%m-%d")}.csv' if incremental else f'/dvdrental/{table_name}.csv'
            bucket_name = 'extracted-data'
            engine = create_engine(PostgresHook(postgres_conn_id='warehouse-db').get_uri())

            try:
                df = CustomMinio._get_dataframe(bucket_name, object_name)
                df = df.set_index(table_pkey[table_name])

                upsert(
                    con=engine,
                    df=df,
                    table_name=table_name,
                    schema='staging',
                    if_row_exists='update'
                )

            except:
                engine.dispose()
                raise AirflowSkipException(f"{table_name} doesn't have new data. Skipped...")

        except AirflowSkipException as e:
            raise e
        
        except Exception as e:
            raise AirflowException(f"Error when loading {table_name} : {str(e)}")