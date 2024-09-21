from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

@dag(
    start_date = days_ago(1), 
    schedule_interval = '@daily'
)
def mapping_multiple_inputs():
    @task
    def process_data(value, multiplier):
        result = value * multiplier
        print(f"Processing {value} with multiplier {multiplier}, result: {result}")

    # Multiple lists for mapping
    values = [1, 2, 3, 4]
    multipliers = [10, 20, 30, 40]

    process_data.expand(value = values, multiplier = multipliers)

mapping_multiple_inputs()