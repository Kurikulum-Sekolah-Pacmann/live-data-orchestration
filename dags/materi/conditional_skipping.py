from airflow.decorators import dag, task
from airflow.exceptions import AirflowSkipException
from airflow.utils.dates import days_ago


@dag(
    dag_id='conditional_skipping',
    start_date=days_ago(1),
    schedule='@daily'
)
def conditional_skipping():
    @task
    def extract_a():
        data_avalilability = True
        if data_avalilability:
            print('data available')
        else:
            raise AirflowSkipException("data isn't available")

    @task
    def extract_b():
        data_avalilability = False
        if data_avalilability:
            print('data available')
        else:
            raise AirflowSkipException("data isn't available")
        
    extract_a() >> extract_b()
    
conditional_skipping()