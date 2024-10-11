from airflow.decorators import task_group
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# Constants
DATE = '{{ ds }}'

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
    'spark.executor.memory': '4g',  # Define RAM per executor
    'spark.executor.cores': '2',  # Define cores per executor
    'spark.scheduler.mode': 'FAIR'
}

@task_group
def warehouse(incremental):
    """
    Task group for the warehouse ETL process.
    """

    @task_group
    def step_1():
        """
        Step 1 of the ETL process: Extract, Transform, Validate, and Load data for categories, customers, and customers_history.
        """

        @task_group
        def extract_transform():
            """
            Extract and transform data for categories, customers, and customers_history.
            """
            tables = ['categories', 'customers', 'customers_history']
            for table in tables:
                SparkSubmitOperator(
                    task_id=f'{table}',
                    conn_id='spark-conn',
                    application=f'dags/etl_pipeline/tasks/warehouse/components/extract_transform.py',
                    application_args=[
                        f'{table}',
                        f'{incremental}',
                        DATE
                    ],
                    conf=spark_conf,
                    jars=','.join(jar_list),
                    trigger_rule='none_failed',
                )

        @task_group
        def validations():
            """
            Validate data for categories, customers, and customers_history.
            """
            validation_tasks = {
                "categories": {
                    "need_validation": False,
                    "columns_to_validate": {}
                },
                "customers": {
                    "need_validation": True,
                    "columns_to_validate": {
                        "email": "validate_email_format",
                        "phone": "validate_phone_format",
                        "credit_card_expiration": "validate_credit_card_expiration_format"
                    }
                },
                "customers_history": {
                    "need_validation": True,
                    "columns_to_validate": {
                        "email": "validate_email_format",
                        "phone": "validate_phone_format",
                        "credit_card_expiration": "validate_credit_card_expiration_format"
                    }
                }
            }

            for table in validation_tasks:
                need_validation = str(validation_tasks[table]["need_validation"])
                valid_bucket = 'valid-data'
                invalid_bucket = 'invalid-data'
                columns_to_validate = str(validation_tasks[table]["columns_to_validate"])

                SparkSubmitOperator(
                    task_id=f'{table}',
                    conn_id='spark-conn',
                    application=f'dags/etl_pipeline/tasks/warehouse/components/validations.py',
                    application_args=[
                        f'{need_validation}',
                        f'{table}',
                        f'{valid_bucket}',
                        f'{invalid_bucket}',
                        f'{columns_to_validate}',
                        f'{incremental}',
                        f'{DATE}'
                    ],
                    conf=spark_conf,
                    jars=','.join(jar_list),
                    trigger_rule='none_failed',
                )

        @task_group
        def load():
            """
            Load data for categories, customers, and customers_history into the warehouse.
            """
            load_tasks = [
                ('categories', ['category_nk']),
                ('customers', ['customer_nk']),
                ('customers_history', ['customer_nk'])
            ]
            for table, table_pkey in load_tasks:
                SparkSubmitOperator(
                    task_id=f'{table}',
                    conn_id='spark-conn',
                    application=f'dags/etl_pipeline/tasks/warehouse/components/load.py',
                    application_args=[
                        f'{table}',
                        ','.join(table_pkey),
                        f'{incremental}',
                        DATE
                    ],
                    conf=spark_conf,
                    jars=','.join(jar_list),
                    trigger_rule='none_failed',
                )

        # Define the order of execution for step 1
        extract_transform() >> validations() >> load()

    @task_group
    def step_2():
        """
        Step 2 of the ETL process: Extract, Transform, Validate, and Load data for products and orders.
        """

        @task_group
        def extract_transform():
            """
            Extract and transform data for products and orders.
            """
            tables = ['products_history', 'orders_history', 'products', 'orders']
            for table in tables:
                SparkSubmitOperator(
                    task_id=f'{table}',
                    conn_id='spark-conn',
                    application=f'dags/etl_pipeline/tasks/warehouse/components/extract_transform.py',
                    application_args=[
                        f'{table}',
                        f'{incremental}',
                        DATE
                    ],
                    conf=spark_conf,
                    jars=','.join(jar_list),
                    trigger_rule='none_failed',
                )

        @task_group
        def validations():
            """
            Validate data for products and orders.
            """
            validation_tasks = {
                "products": {
                    "need_validation": True,
                    "columns_to_validate": {
                        "price": "validate_price_range"
                    }
                },
                "orders": {
                    "need_validation": True,
                    "columns_to_validate": {
                        "net_amount": "validate_positive_value",
                        "tax": "validate_positive_value",
                        "total_amount": "validate_positive_value"
                    }
                },
                "products_history": {
                    "need_validation": True,
                    "columns_to_validate": {
                        "price": "validate_price_range"
                    }
                },
                "orders_history": {
                    "need_validation": True,
                    "columns_to_validate": {
                        "net_amount": "validate_positive_value",
                        "tax": "validate_positive_value",
                        "total_amount": "validate_positive_value"
                    }
                }
            }

            for table_name in validation_tasks:
                need_validation = str(validation_tasks[table_name]["need_validation"])
                valid_bucket = 'valid-data'
                invalid_bucket = 'invalid-data'
                columns_to_validate = str(validation_tasks[table_name]["columns_to_validate"])

                SparkSubmitOperator(
                    task_id=f'{table_name}',
                    conn_id='spark-conn',
                    application=f'dags/etl_pipeline/tasks/warehouse/components/validations.py',
                    application_args=[
                        f'{need_validation}',
                        f'{table_name}',
                        f'{valid_bucket}',
                        f'{invalid_bucket}',
                        f'{columns_to_validate}',
                        f'{incremental}',
                        f'{DATE}'
                    ],
                    conf=spark_conf,
                    jars=','.join(jar_list),
                    trigger_rule='none_failed',
                )

        @task_group
        def load():
            """
            Load data for products and orders into the warehouse.
            """
            load_tasks = [
                ('products_history', ['product_nk']),
                ('orders_history', ['order_nk']),
                ('products', ['product_nk']),
                ('orders', ['order_nk'])
            ]
            for table, table_pkey in load_tasks:
                SparkSubmitOperator(
                    task_id=f'{table}',
                    conn_id='spark-conn',
                    application=f'dags/etl_pipeline/tasks/warehouse/components/load.py',
                    application_args=[
                        f'{table}',
                        ','.join(table_pkey),
                        f'{incremental}',
                        DATE
                    ],
                    conf=spark_conf,
                    jars=','.join(jar_list),
                    trigger_rule='none_failed',
                )

        # Define the order of execution for step 2
        extract_transform() >> validations() >> load()

    @task_group
    def step_3():
        """
        Step 3 of the ETL process: Extract, Transform, Validate, and Load data for inventory, orderlines, cust_hist, and order_status_analytic.
        """

        @task_group
        def extract_transform():
            """
            Extract and transform data for inventory, orderlines, cust_hist, and order_status_analytic.
            """
            tables = ['inventory', 'orderlines', 'cust_hist', 'order_status_analytic']
            for table in tables:
                SparkSubmitOperator(
                    task_id=f'{table}',
                    conn_id='spark-conn',
                    application=f'dags/etl_pipeline/tasks/warehouse/components/extract_transform.py',
                    application_args=[
                        f'{table}',
                        f'{incremental}',
                        DATE
                    ],
                    conf=spark_conf,
                    jars=','.join(jar_list),
                    trigger_rule='none_failed',
                )

        @task_group
        def validations():
            """
            Validate data for inventory, orderlines, cust_hist, and order_status_analytic.
            """
            validation_tasks = {
                "inventory": {
                    "need_validation": False,
                    "columns_to_validate": {}
                },
                "orderlines": {
                    "need_validation": True,
                    "columns_to_validate": {
                        "quantity": "validate_positive_value"
                    }
                },
                "cust_hist": {
                    "need_validation": False,
                    "columns_to_validate": {}
                },
                "order_status_analytic": {
                    "need_validation": True,
                    "columns_to_validate": {
                        "status": "validate_order_status"
                    }
                }
            }

            for table in validation_tasks:
                need_validation = str(validation_tasks[table]["need_validation"])
                valid_bucket = 'valid-data'
                invalid_bucket = 'invalid-data'
                columns_to_validate = str(validation_tasks[table]["columns_to_validate"])

                SparkSubmitOperator(
                    task_id=f'{table}',
                    conn_id='spark-conn',
                    application=f'dags/etl_pipeline/tasks/warehouse/components/validations.py',
                    application_args=[
                        f'{need_validation}',
                        f'{table}',
                        f'{valid_bucket}',
                        f'{invalid_bucket}',
                        f'{columns_to_validate}',
                        f'{incremental}',
                        f'{DATE}'
                    ],
                    conf=spark_conf,
                    jars=','.join(jar_list),
                    trigger_rule='none_failed',
                )

        @task_group
        def load():
            """
            Load data for inventory, orderlines, cust_hist, and order_status_analytic into the warehouse.
            """
            load_tasks = [
                ('inventory', ['product_nk']),
                ('orderlines', ['orderline_nk', 'order_id', 'product_id', 'quantity']),
                ('cust_hist', ['customer_id', 'order_id', 'product_id']),
                ('order_status_analytic', ['order_id'])
            ]
            for table, table_pkey in load_tasks:
                SparkSubmitOperator(
                    task_id=f'{table}',
                    conn_id='spark-conn',
                    application=f'dags/etl_pipeline/tasks/warehouse/components/load.py',
                    application_args=[
                        f'{table}',
                        f'{table_pkey}',
                        f'{incremental}',
                        f'{DATE}'
                    ],
                    conf=spark_conf,
                    jars=','.join(jar_list),
                    trigger_rule='none_failed',
                )

        # Define the order of execution for step 3
        extract_transform() >> validations() >> load()

    # Define the order of execution for the steps
    step_1() >> step_2() >> step_3()