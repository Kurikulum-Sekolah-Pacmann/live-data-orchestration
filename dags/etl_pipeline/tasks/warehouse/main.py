from airflow.decorators import task_group
from airflow.operators.python import PythonOperator

from etl_pipeline.tasks.warehouse.components.extract_transform import ExtractTransform 
from etl_pipeline.tasks.warehouse.components.validations import Validation, ValidationType
from etl_pipeline.tasks.warehouse.components.load import Load


@task_group
def warehouse(incremental):
    @task_group
    def step_1():
        @task_group
        def extract_transform():
            tasks = [
                ('categories', ExtractTransform._categories),
                ('customers', ExtractTransform._customers),
                ('products', ExtractTransform._products),
                ('orders', ExtractTransform._orders),
                ('customers_history', ExtractTransform._customers_history),
                ('products_history', ExtractTransform._products_history),
                ('orders_history', ExtractTransform._orders_history)
            ]

            for task_id, python_callable in tasks:
                PythonOperator(
                    task_id=task_id,
                    python_callable=python_callable,
                    op_kwargs={
                        'incremental': incremental,
                        'date': '{{ ds }}'
                    }
                )

        @task_group
        def validation():
            validation_tasks = [
                ('categories', 'categories.csv', False, {}),
                ('customers', 'customers.csv', True, {
                    "email": ValidationType.validate_email_format, 
                    "phone": ValidationType.validate_phone_format, 
                    "credit_card_expiration": ValidationType.validate_credit_card_expiration_format
                }),
                ('products', 'products.csv', True, {
                    "price": ValidationType.validate_price_range
                }),
                ('orders', 'orders.csv', True, {
                    "net_amount": ValidationType.validate_positive_value,
                    "tax": ValidationType.validate_positive_value,
                    "total_amount": ValidationType.validate_positive_value
                }),
                ('customers_history', 'customers_history.csv', True, {
                    "email": ValidationType.validate_email_format, 
                    "phone": ValidationType.validate_phone_format, 
                    "credit_card_expiration": ValidationType.validate_credit_card_expiration_format
                }),
                ('products_history', 'products_history.csv', True, {
                    "price": ValidationType.validate_price_range
                }),
                ('orders_history', 'orders_history.csv', True, {
                    "net_amount": ValidationType.validate_positive_value,
                    "tax": ValidationType.validate_positive_value,
                    "total_amount": ValidationType.validate_positive_value
                })
            ]

            for task_id, data, need_validation, validation_functions in validation_tasks:
                PythonOperator(
                    task_id=task_id,
                    python_callable=Validation._data_validations,
                    op_kwargs={
                        'need_validation': need_validation,
                        'data': data,
                        'valid_bucket': 'valid-data',
                        'dest_object': data,
                        'invalid_bucket': 'invalid-data' if need_validation else None,
                        'validation_functions': validation_functions if need_validation else None
                    }
                )

        @task_group
        def load():
            categories = PythonOperator(
                task_id = 'categories',
                python_callable = Load._warehouse,
                trigger_rule = 'none_failed',
                op_kwargs = {
                    'table_name': 'categories',
                    'incremental': incremental,
                    'table_pkey': 'category_nk',
                    'date': '{{ ds }}'
                }
            )

            customers = PythonOperator(
                task_id = 'customers',
                python_callable = Load._warehouse,
                trigger_rule = 'none_failed',
                op_kwargs = {
                    'table_name': 'customers',
                    'incremental': incremental,
                    'table_pkey': 'customer_nk',
                    'date': '{{ ds }}'
                }   
            )

            products = PythonOperator(
                task_id = 'products',
                python_callable = Load._warehouse,
                trigger_rule = 'none_failed',
                op_kwargs = {
                    'table_name': 'products',
                    'incremental': incremental,
                    'table_pkey': 'product_nk',
                    'date': '{{ ds }}'
                }
            )

            orders = PythonOperator(
                task_id = 'orders',
                python_callable = Load._warehouse,
                trigger_rule = 'none_failed',
                op_kwargs = {
                    'table_name': 'orders',
                    'incremental': incremental,
                    'table_pkey': 'order_nk',
                    'date': '{{ ds }}'
                }
            )

            customers_history = PythonOperator(
                task_id = 'customers_history',
                python_callable = Load._warehouse,
                trigger_rule = 'none_failed',
                op_kwargs = {
                    'table_name': 'customers',
                    'incremental': incremental,
                    'table_pkey': 'customer_nk',
                    'date': '{{ ds }}'
                }
            )

            products_history = PythonOperator(
                task_id = 'products_history',
                python_callable = Load._warehouse,
                trigger_rule = 'none_failed',
                op_kwargs = {
                    'table_name': 'products',
                    'incremental': incremental,
                    'table_pkey': 'product_nk',
                    'date': '{{ ds }}'
                }
            )

            orders_history = PythonOperator(
                task_id = 'orders_history',
                python_callable = Load._warehouse,
                trigger_rule = 'none_failed',
                op_kwargs = {
                    'table_name': 'orders',
                    'incremental': incremental,
                    'table_pkey': 'order_nk',
                    'date': '{{ ds }}'
                }
            )

            categories >> products_history >> products
            customers_history >> customers >> orders_history >>orders
            

        extract_transform() >> validation() >> load()


    @task_group
    def step_2():
        @task_group
        def extract_transform():
            tasks = [
                ('inventory', ExtractTransform._inventory),
                ('orderlines', ExtractTransform._orderlines),
                ('cust_hist', ExtractTransform._cust_hist),
                ('order_status_analytic', ExtractTransform._order_status_analytic)
            ]

            for task_id, python_callable in tasks:
                PythonOperator(
                    task_id=task_id,
                    python_callable=python_callable,
                    op_kwargs={
                        'incremental': incremental,
                        'date': '{{ ds }}'
                    }
                )
            

        @task_group
        def validation():
            validation_tasks = [
                ('inventory', 'inventory.csv', False, {}),
                ('orderlines', 'orderlines.csv', True, {
                    "quantity": ValidationType.validate_positive_value
                }),
                ('cust_hist', 'cust_hist.csv', False, {}),
                ('order_status_analytic', 'order_status_analytic.csv', True, {
                    "status": ValidationType.validate_order_status
                })
            ]

            for task_id, data, need_validation, validation_functions in validation_tasks:
                PythonOperator(
                    task_id=task_id,
                    python_callable=Validation._data_validations,
                    op_kwargs={
                        'need_validation': need_validation,
                        'data': data,
                        'valid_bucket': 'valid-data',
                        'dest_object': data,
                        'invalid_bucket': 'invalid-data' if need_validation else None,
                        'validation_functions': validation_functions if need_validation else None
                    }
                )

        @task_group
        def load():
            load_tasks = [
                ('inventory', 'product_nk'),
                ('orderlines', ["orderline_nk", "order_id", "product_id", "quantity"]),
                ('cust_hist', ["customer_id", "order_id", "product_id"]),
                ('order_status_analytic', 'order_id')
            ]

            for task_id, table_pkey in load_tasks:
                PythonOperator(
                    task_id=task_id,
                    python_callable=Load._warehouse,
                    trigger_rule='none_failed',
                    op_kwargs={
                        'table_name': task_id,
                        'incremental': incremental,
                        'table_pkey': table_pkey,
                        'date': '{{ ds }}'
                    }
                )
            

        extract_transform() >> validation() >> load()

    step_1() >> step_2()