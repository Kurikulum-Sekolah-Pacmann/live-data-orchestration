from airflow.decorators import dag, task
from airflow.operators.python import ExternalPythonOperator
from datetime import datetime

@dag(
    start_date = datetime.now(),
    schedule = "@once"
)
def external_python_2():
    @task.external_python(
        python = "/dags_venv/materi/venv/bin/python" # Specify the path to the python interpreter
    )
    def check_numpy_version():
        import numpy as np
        print(np.__version__)

    @task
    def check_numpy_version2():
        import numpy as np
        print(np.__version__)

    check_numpy_version() >> check_numpy_version2()

external_python_2()