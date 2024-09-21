from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

@dag(
    start_date=days_ago(1), 
    schedule_interval='@daily'
)
def dynamic_task_mapping_1():
    @task
    def extract(table_name):
        print(f"Extract data: {table_name}")

    # Input
    table_to_extract = ["customers", "orders", "products", "order_details"]

    # Map over the input and create multiple tasks instances
    extract.expand(table_name = table_to_extract)

dynamic_task_mapping_1()