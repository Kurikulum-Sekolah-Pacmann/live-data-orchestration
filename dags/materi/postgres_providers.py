from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import pandas as pd

@dag(
    start_date = days_ago(1),
    schedule_interval = '@daily'
)
def postgres_providers():
    @task
    def get_data():
        hook = PostgresHook(postgres_conn_id = 'dellstore_db')
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        return df

    get_data()

postgres_providers()