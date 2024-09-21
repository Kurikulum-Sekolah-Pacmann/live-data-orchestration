from airflow.decorators import dag, task
from airflow.operators.python import PythonVirtualenvOperator
from datetime import datetime

def numpy_version():
    import numpy as np
    print(np.__version__)

@dag(
    start_date = datetime.now(),
    schedule = "@once"
)
def virtual_env_1():
    check_numpy_version = PythonVirtualenvOperator(
        task_id='check_numpy_version',
        python_callable=numpy_version,
        requirements=['numpy==2.1.1'] # Specify the version of numpy to be installed
    )

    @task
    def check_numpy_version2():
        import numpy as np
        print(np.__version__)
    
    check_numpy_version >> check_numpy_version2()

virtual_env_1()