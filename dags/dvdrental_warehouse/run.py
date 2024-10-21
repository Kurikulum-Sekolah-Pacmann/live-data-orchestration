from datetime import datetime
from airflow.datasets import Dataset
from helper.callbacks.slack_notifier import slack_notifier

from cosmos.config import ProjectConfig, ProfileConfig, RenderConfig
from cosmos.profiles.postgres import PostgresUserPasswordProfileMapping
from cosmos import DbtDag

import os

DBT_PROJECT_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/dvdrental_warehouse/dvdrental_dbt"

project_config = ProjectConfig(
    dbt_project_path=DBT_PROJECT_PATH,
    project_name="dvdrental_warehouse"
)

profile_config = ProfileConfig(
    profile_name="warehouse",
    target_name="warehouse",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id='warehouse-db',
        profile_args={"schema": "warehouse"}
    )
)

dag = DbtDag(
    dag_id="dvdrental_warehouse",
    schedule=[
        Dataset("postgres://warehouse-db:5432/warehouse.staging.actor"),
        Dataset("postgres://warehouse-db:5432/warehouse.staging.address"),
        Dataset("postgres://warehouse-db:5432/warehouse.staging.category"),
        Dataset("postgres://warehouse-db:5432/warehouse.staging.city"),
        Dataset("postgres://warehouse-db:5432/warehouse.staging.country"),
        Dataset("postgres://warehouse-db:5432/warehouse.staging.customer"),
        Dataset("postgres://warehouse-db:5432/warehouse.staging.film"),
        Dataset("postgres://warehouse-db:5432/warehouse.staging.film_actor"),
        Dataset("postgres://warehouse-db:5432/warehouse.staging.film_category"),
        Dataset("postgres://warehouse-db:5432/warehouse.staging.inventory"),
        Dataset("postgres://warehouse-db:5432/warehouse.staging.language"),
        Dataset("postgres://warehouse-db:5432/warehouse.staging.payment"),
        Dataset("postgres://warehouse-db:5432/warehouse.staging.rental"),
        Dataset("postgres://warehouse-db:5432/warehouse.staging.staff"),
        Dataset("postgres://warehouse-db:5432/warehouse.staging.store")
    ],
    catchup=False,
    start_date=datetime(2024, 10, 1),
    project_config=project_config,
    profile_config=profile_config,
    render_config=RenderConfig(
        dbt_executable_path="/opt/airflow/dbt_venv/bin",
        emit_datasets=True
    ),
    default_args={
        'on_failure_callback': slack_notifier
    }
)