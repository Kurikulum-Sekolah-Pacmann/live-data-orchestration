from airflow.decorators import task_group
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from dvdrental_staging.tasks.components.extract import Extract
from dvdrental_staging.tasks.components.load import Load
from airflow.datasets import Dataset

@task_group
def extract(incremental):            
    table_to_extract = eval(Variable.get('list_dvdrental_table'))

    for table_name in table_to_extract:
        current_task = PythonOperator(
            task_id = f'{table_name}',
            python_callable = Extract._dvdrental,
            trigger_rule = 'none_failed',
            op_kwargs = {
                'table_name': f'{table_name}',
                'incremental': incremental
            }
        )

        current_task

@task_group
def load(incremental):
    table_to_load = eval(Variable.get('list_dvdrental_table'))
    table_pkey = eval(Variable.get('pkey_dvdrental_table'))
    previous_task = None
    
    for table_name in table_to_load:
        current_task = PythonOperator(
            task_id = f'{table_name}',
            python_callable = Load._dvdrental,
            trigger_rule = 'none_failed',
            outlets = [Dataset(f'postgres://warehouse-db:5432/warehouse.staging.{table_name}')],
            op_kwargs = {
                'table_name': table_name,
                'table_pkey': table_pkey,
                'incremental': incremental
            },
        )

        if previous_task:
            previous_task >> current_task

        previous_task = current_task