from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SQLExecuteQueryOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'snowflake_conn_id': 'snow_connection'
}

with DAG(
    'snowflake_simple_insert',
    default_args=default_args,
    description='A DAG that only inserts data into Snowflake',
    schedule=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['snowflake', 'insert'],
) as dag:

    create_table = SQLExecuteQueryOperator(
    task_id='create_table',
    sql="""
    CREATE TABLE IF NOT EXISTS Testing_Table (
        id INT,
        name STRING,
        created_at TIMESTAMP
    )
    """,
    autocommit=True,
    conn_id='snow_connection'
)

insert_data = SQLExecuteQueryOperator(
    task_id='insert_data',
    sql="""
    INSERT INTO Testing_Table (id, name, created_at)
    VALUES 
        (1, 'First record', CURRENT_TIMESTAMP()),
        (2, 'Second record', CURRENT_TIMESTAMP()),
        (3, 'Third record', CURRENT_TIMESTAMP())
    """,
    autocommit=True,
    conn_id='snow_connection'
)

# Set task order
create_table >> insert_data
