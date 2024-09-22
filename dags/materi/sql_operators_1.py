from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime

@dag(
    dag_id = 'sql_operators_1',
    start_date = datetime(2024, 9, 1),
    schedule = "@once"
)
def sql_operators_1():
    create_and_insert = SQLExecuteQueryOperator(
        task_id = 'create_and_insert',
        conn_id = "staging_db",
        sql = """
            CREATE TABLE IF NOT EXISTS test (id INT, name VARCHAR(255));
            INSERT INTO test (id, name) VALUES (1, 'John'), (2, 'Doe');
        """
    )
    select_data = SQLExecuteQueryOperator(
        task_id = 'select_data',
        conn_id = "staging_db",
        sql = "SELECT * FROM test;",
        show_return_value_in_logs = True
    )

    create_and_insert >> select_data

sql_operators_1()