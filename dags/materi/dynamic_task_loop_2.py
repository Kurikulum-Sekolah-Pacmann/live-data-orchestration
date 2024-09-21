from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

@task(task_id='process_')
def process_dataset(dataset_name):
    print(f"Processing dataset: {dataset_name}")

table_to_extract = ["customers", "orders", "products", "order_details"]

@dag(
        start_date=days_ago(1), 
        schedule_interval='@daily'
)

def dynamic_task_loop_2():
    for dataset in table_to_extract:
        process_dataset.override(task_id=f'process_{dataset}')(dataset)

dynamic_task_loop_2()