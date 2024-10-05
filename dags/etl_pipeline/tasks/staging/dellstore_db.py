from airflow.decorators import task_group
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from etl_pipeline.tasks.staging.components.extract import Extract
from etl_pipeline.tasks.staging.components.load import Load
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

@task_group
def dellstore_db(incremental):
    """
    Task group to handle the extraction and loading of Dellstore database data.

    Args:
        incremental (bool): Flag to indicate if the process is incremental.
    """

    @task_group
    def extract():
        """
        Task group to handle the extraction of data from Dellstore database.
        """
        # Get the list of tables to extract from Airflow Variable
        table_to_extract = eval(Variable.get('list_dellstore_table'))

        # Define the list of JAR files required for Spark
        jar_list = [
            '/opt/spark/jars/hadoop-aws-3.3.1.jar',
            '/opt/spark/jars/aws-java-sdk-bundle-1.11.901.jar',
            '/opt/spark/jars/postgresql-42.2.23.jar'
        ]

        # Define Spark configuration
        spark_conf = {
            'spark.hadoop.fs.s3a.access.key': 'minio',
            'spark.hadoop.fs.s3a.secret.key': 'minio123',
            'spark.hadoop.fs.s3a.endpoint': 'http://minio:9000',
            'spark.hadoop.fs.s3a.path.style.access': 'true',
            'spark.hadoop.fs.s3a.impl': 'org.apache.hadoop.fs.s3a.S3AFileSystem',
            'spark.dynamicAllocation.enabled': 'true',
            'spark.dynamicAllocation.maxExecutors': '3',
            'spark.dynamicAllocation.minExecutors': '1',
            'spark.dynamicAllocation.initialExecutors': '1',
            'spark.scheduler.mode': 'FAIR'
        }

        # Create a SparkSubmitOperator for each table to extract
        for table_name in table_to_extract:
            SparkSubmitOperator(
                task_id=table_name,
                conn_id="spark-conn",
                application="dags/etl_pipeline/tasks/staging/components/extract.py",
                application_args=[
                    table_name,
                    str(incremental)
                ],
                conf=spark_conf,
                jars=','.join(jar_list),
                trigger_rule='none_failed'
            )

    @task_group
    def load():
        """
        Task group to handle the loading of data into Dellstore database.
        """
        # Get the list of tables to load and their primary keys from Airflow Variable
        table_to_load = eval(Variable.get('list_dellstore_table'))
        table_pkey = eval(Variable.get('pkey_dellstore_table'))

        # Define the list of JAR files required for Spark
        jar_list = [
            '/opt/spark/jars/hadoop-aws-3.3.1.jar',
            '/opt/spark/jars/aws-java-sdk-bundle-1.11.901.jar',
            '/opt/spark/jars/postgresql-42.2.23.jar'
        ]

        # Define Spark configuration
        spark_conf = {
            'spark.hadoop.fs.s3a.access.key': 'minio',
            'spark.hadoop.fs.s3a.secret.key': 'minio123',
            'spark.hadoop.fs.s3a.endpoint': 'http://minio:9000',
            'spark.hadoop.fs.s3a.path.style.access': 'true',
            'spark.hadoop.fs.s3a.impl': 'org.apache.hadoop.fs.s3a.S3AFileSystem'
        }

        previous_task = None

        # Create a SparkSubmitOperator for each table to load
        for table_name in table_to_load:
            current_task = SparkSubmitOperator(
                task_id=table_name,
                conn_id="spark-conn",
                application="dags/etl_pipeline/tasks/staging/components/load.py",
                application_args=[
                    table_name,
                    str(table_pkey[table_name]),
                    str(incremental),
                    '{{ ds }}'
                ],
                conf=spark_conf,
                jars=','.join(jar_list),
                trigger_rule='none_failed'
            )

            # Set task dependencies
            if previous_task:
                previous_task >> current_task

            previous_task = current_task

    # Define the task dependencies between extract and load task groups
    extract() >> load()