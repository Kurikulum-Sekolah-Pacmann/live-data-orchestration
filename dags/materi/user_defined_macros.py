from airflow.decorators import dag, task
from datetime import datetime

def custom_greet(name):
    return f"Hello {name}"

@dag(
    dag_id = 'user_defined_macros_example',
    start_date = datetime.now(),
    schedule = "@once",
    catchup = False,
    user_defined_macros={
        "greet": custom_greet  # Defining the custom macro
    }
)
def user_defined_macros_example():

    @task()
    def print_data(data):
        print(data)

    print_hello_world = (
        print_data
        .override(task_id='print_hello_world')
        ('{{ greet("World") }}')
    )

    print_hello_pacmann = (
        print_data
        .override(task_id='print_hello_pacmann')
        ('{{ greet("Pacmann") }}')
    )

    print_hello_world >> print_hello_pacmann

user_defined_macros_example()