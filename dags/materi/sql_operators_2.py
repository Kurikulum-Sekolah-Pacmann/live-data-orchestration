from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLValueCheckOperator
from datetime import datetime

@dag(
    dag_id = 'sql_operators_2',
    start_date = datetime(2024, 9, 1),
    schedule = "@once"
)
def sql_operators_2():
    check_data = SQLValueCheckOperator(
        task_id = 'check_data',
        conn_id = 'staging_db',
        sql = "SELECT COUNT(DISTINCT name) AS names FROM test;",
        pass_value = 3,
        tolerance = 1
    )

sql_operators_2()