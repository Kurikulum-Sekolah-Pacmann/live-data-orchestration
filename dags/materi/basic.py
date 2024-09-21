from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

def extract(table_name):
    print(f"Extract process: {table_name}")


@dag(
        start_date=days_ago(1), 
        schedule='@daily'
)

def example_dags():
    customers = PythonOperator(
        task_id='customers',
        python_callable=extract,
        op_args=['customers']
    )

    orders = PythonOperator(
        task_id='orders',
        python_callable=extract,
        op_args=['orders']
    )

    products = PythonOperator(
        task_id='products',
        python_callable=extract,
        op_args=['products']
    )

    order_details = PythonOperator(
        task_id='order_details',
        python_callable=extract,
        op_args=['order_details']
    )

example_dags()