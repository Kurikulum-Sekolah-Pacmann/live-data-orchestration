from airflow.decorators import dag, task, task_group
from datetime import datetime
import time
# Define the DAG using the dag decorator
@dag(
    description='A simple DAG',
    schedule_interval='*/5 * * * *',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['example']
)
def example_dag():
    
    @task
    def task_1():
        time.sleep(10)
        print("This is task 1")
    
    @task
    def task_2():
        time.sleep(20)
        print("This is task 2")

    @task_group
    def task_groups():
        @task
        def task_3():
            time.sleep(30)
            print("This is task 3")

        @task
        def task_4():
            time.sleep(40)
            print("This is task 4")

        task_3() >> task_4()

    
    task_1() >> task_2() >> task_groups()

example_dag()