from airflow.decorators import dag, task
from pendulum import datetime
from airflow.operators.bash import BashOperator

var_1 = '{{ var.value.var_1 }}'

@dag(
    dag_id = 'templates_with_jinja',
    description = 'Jinja templating examples',
    start_date = datetime(2024, 9, 1),
    schedule = "@once"
)
def templates_with_jinja():
    get_dates = BashOperator(
        task_id='dates',
        bash_command='echo dates : {{ ds }}'
    )

    @task
    def print_var_1(value):
        print(value)

    get_dates >> print_var_1(value = var_1)

templates_with_jinja()