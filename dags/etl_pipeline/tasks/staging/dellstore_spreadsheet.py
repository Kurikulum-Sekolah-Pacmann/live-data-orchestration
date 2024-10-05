from airflow.decorators import task_group
from airflow.operators.python import PythonOperator
from etl_pipeline.tasks.staging.components.extract import Extract
from etl_pipeline.tasks.staging.components.load import Load

@task_group
def dellstore_spreadsheet():
    """
    Task group for Dellstore Spreadsheet Extract and Load process.
    """

    # Define the extract task
    extract = PythonOperator(
        task_id='extract',
        python_callable=Extract._dellstore_spreadsheet,
        trigger_rule='none_failed'
    )

    # Define the load task
    load = PythonOperator(
        task_id='load',
        python_callable=Load._dellstore_spreadsheet,
        trigger_rule='none_failed'
    )

    # Set the task dependencies
    extract >> load