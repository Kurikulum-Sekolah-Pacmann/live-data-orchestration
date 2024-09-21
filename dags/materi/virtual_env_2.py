from airflow.decorators import dag, task
from datetime import datetime

@dag(
    start_date = datetime.now(),
    schedule = "@once"
)
def virtual_env_2():
    @task.virtualenv(requirements=['numpy==2.1.1'])
    def check_numpy_version():
        import numpy as np
        print(np.__version__)

    @task
    def check_numpy_version2():
        import numpy as np
        print(np.__version__)
    
    check_numpy_version() >> check_numpy_version2()

virtual_env_2()