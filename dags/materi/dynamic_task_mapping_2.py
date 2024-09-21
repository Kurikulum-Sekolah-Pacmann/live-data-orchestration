from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

@dag(
        start_date=days_ago(1), 
        schedule_interval='@daily'
)
def dynamic_task_mapping_2():
    def extract(table_name):
        print(f"Extract data: {table_name}")

    # Input
    table_to_extract = ["customers", "orders", "products", "order_details"]

    extract_task = PythonOperator.partial(
        task_id = 'extract',
        python_callable = extract
    ).expand(op_args = [[table_name] for table_name in table_to_extract])

dynamic_task_mapping_2()