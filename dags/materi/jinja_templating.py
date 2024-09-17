from airflow.decorators import dag, task
from pendulum import datetime
from airflow.operators.bash import BashOperator

var_1 = '{{ var.value.var_1 }}'

@dag(
    dag_id = 'jinja_templating',
    description = 'Jinja templating examples',
    start_date = datetime(2024, 9, 1),
    schedule = "@once"
)
def jinja_templating():
    dates = BashOperator(
        task_id='dates',
        bash_command='echo dates : {{ ds }}'
    )

    data_interval_start = BashOperator(
        task_id='date_interval_start',
        bash_command='echo data_interval_start : {{ data_interval_start }}'
    )

    @task
    def print_var_1(value):
        print(value)

    dates >> data_interval_start >> print_var_1(value = var_1)

jinja_templating()