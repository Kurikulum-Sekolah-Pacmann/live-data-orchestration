from cosmos.config import ProjectConfig, ProfileConfig
from cosmos.profiles.postgres import PostgresUserPasswordProfileMapping
from cosmos import DbtDag
from cosmos.constants import TestBehavior
from datetime import datetime
from cosmos.config import RenderConfig
import os

DBT_PROJECT_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/materi/dbt_airflow/dbt/jaffle_shop"


profile_config = ProfileConfig(
    profile_name="jaffle_shop",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id='warehouse-db',
        profile_args={"schema": "jaffle_shop"}
    )
)

project_config = ProjectConfig(
    dbt_project_path=DBT_PROJECT_PATH,
    project_name="jaffle_shop"
)

render_config = RenderConfig(
    dbt_executable_path="/opt/airflow/dbt_venv/bin/",
    test_behavior=TestBehavior.AFTER_ALL
)

dag = DbtDag(
    dag_id="dbt_jaffle_shop",
    schedule="@daily",
    catchup=False,
    start_date=datetime(2024, 10, 1),
    project_config=project_config,
    profile_config=profile_config,
    render_config=render_config
)