from airflow.decorators import dag, task
from airflow.exceptions import AirflowSkipException
from airflow.utils.dates import days_ago

@task
def extract(avalilability):
    if avalilability:
        print('data is available')
    else:
        raise AirflowSkipException("data isn't available")

@dag(
    start_date=days_ago(1),
    schedule='@daily'
)
def trigger_rules():
    extract_a = extract.override(task_id = 'extract_a')(avalilability = True)
    extract_b = extract.override(task_id = 'extract_b')(avalilability = False)

    @task(trigger_rule = "one_success")
    def merge_data():
        print("merge data success")
    
    @task
    def load_data():
        print("load data success")

    [extract_a, extract_b] >> merge_data() >> load_data()
    
trigger_rules()