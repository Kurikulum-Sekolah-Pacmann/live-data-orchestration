from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

def extract(table_name):
    print(f"Extract process: {table_name}")

table_to_extract = ["customers", "orders", "products", "order_details"]

@dag(
        start_date=days_ago(1), 
        schedule='@daily'
)

def dynamic_task_loop_1():
    previous_tasks = None
    for table_name in table_to_extract:
        current_tasks = PythonOperator(
            task_id=f'{table_name}',
            python_callable=extract,
            op_args=[table_name]
        )
        if previous_tasks:
            previous_tasks >> current_tasks
            
        previous_tasks = current_tasks

dynamic_task_loop_1()