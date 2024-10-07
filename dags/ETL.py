from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

TAGS= ["BCRA ETL"]
DAG_ID = "BCRA_ETL"
DAG_DESCRIPTION = """Se extrae datos del Banco """
DAG_SCHEDULE = "* * * * *"
default_args = {
    "start_date":datetime(2024,7,1)
}
retries= 6
retry_delay = timedelta(minutes=20)


#prueba
def task():
    print("hola")

dag = DAG(
    dag_id = DAG_ID,
    description = DAG_DESCRIPTION,
    catchup =True,
    schedule_interval = DAG_SCHEDULE,
    max_active_runs=1,
    dagrun_timeout=timedelta(seconds=200000),
    default_args=default_args,
    tags=TAGS
)

with dag as dag :
    start_task=EmptyOperator(
        task_id="inicia_el_proceso"
    )
    end_task = EmptyOperator(
        task_id="finaliza_el_proceso"
    )
    first_task = PythonOperator(
        task_id = "first_task",
        python_callable=task,
        retries=retries,
        retry_delay=retry_delay
    )

start_task >> first_task >> end_task