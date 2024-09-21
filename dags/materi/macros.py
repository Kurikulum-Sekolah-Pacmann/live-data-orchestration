from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id = 'macros_examples',
    start_date = datetime.now(),
    schedule = "@once",
    catchup = False
)
def macros_example():

    @task()
    def print_data(data):
        print(data)

    task_1 = (
        print_data
        .override(task_id='format_date')
        ('{{ macros.ds_format(ds, "%Y-%m-%d", "%Y/%m/%d") }}')
    )
    task_2 = (
        print_data
        .override(task_id='add_days')
        ('{{ macros.ds_add(ds, 2) }}')
    )
    task_3 = (
        print_data
        .override(task_id='generate_uuid')
        ('{{ macros.uuid.uuid4() }}')
    )

    task_1 >> task_2 >> task_3

macros_example()