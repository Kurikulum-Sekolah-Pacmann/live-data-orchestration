from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

@dag(
    start_date = days_ago(1), 
    schedule_interval = '@daily'
)
def mapping_multiple_inputs_2():
    @task
    def process_data(value, multiplier):
        result = value * multiplier
        return result

    @task
    def pull_data(results):
        print(f"Pulled results: {results}")

    # Multiple lists for mapping
    values = [1, 2, 3, 4]
    multipliers = [10, 20, 30, 40]

    processed_results = process_data.expand(value = values, multiplier = multipliers)
    pull_data(processed_results)

mapping_multiple_inputs_2()