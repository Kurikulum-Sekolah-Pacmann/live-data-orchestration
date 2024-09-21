from airflow.decorators import dag, task
from airflow.operators.python import ExternalPythonOperator
from datetime import datetime

def numpy_version():
    import numpy as np
    print(np.__version__)

@dag(
    start_date = datetime.now(),
    schedule = "@once"
)
def external_python_1():
    check_numpy_version = ExternalPythonOperator(
        task_id ='check_numpy_version',
        python = "/dags_venv/materi/venv/bin/python", # Specify the path to the python interpreter
        python_callable = numpy_version,
    )

    @task
    def check_numpy_version2():
        import numpy as np
        print(np.__version__)

    check_numpy_version >> check_numpy_version2()

external_python_1()