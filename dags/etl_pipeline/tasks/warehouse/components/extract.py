from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.exceptions import AirflowSkipException, AirflowException

import pandas as pd

def _extract(connection_id, table_name, incremental, date = None):
    try:
        pg_hook = PostgresHook(postgres_conn_id = connection_id)
        connection = pg_hook.get_conn()
        cursor = connection.cursor()

        query = f"SELECT * FROM {table_name}"
        if incremental and table_name != 'order_status_analytic':
            query += f" WHERE created_at::DATE = '{date}'::DATE - INTERVAL '1 DAY';"

        cursor.execute(query)
        result = cursor.fetchall()
        column_list = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(result, columns=column_list)

        cursor.close()
        connection.commit()
        connection.close()

        if df.empty:
            raise AirflowSkipException(f"{table_name} doesn't have new data. Skipped...")
        
        else:
            return df
        
    except AirflowSkipException as e:
        raise e

    except Exception as e:
        raise AirflowException(f"Error when extracting data from {table_name}: {e}")