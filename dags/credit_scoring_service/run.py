import datetime
from credit_scoring_service import extraction, preprocessing, training
from airflow.decorators import dag

@dag(
    dag_id = "credit-scoring-service",
    schedule = "@daily",
    start_date = datetime.datetime(2024, 10, 24),
    catchup = False
)
def credit_scoring_service():
    extraction.extract_credit_data() >> preprocessing.preprocess_credit_data() >> training.training_credit_data()

credit_scoring_service()