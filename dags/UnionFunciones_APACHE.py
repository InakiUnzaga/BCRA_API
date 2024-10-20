from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Nivel_1.extraer_BCRA import data_BCRA,maestro_bcra
from Nivel_1.extraer_Feriados import feriado
from Nivel_2.TransformBCRA import transformacion_Pd_Parquet_BCRA
from Nivel_3.LoadBCRA import load_BCRA


TAGS= ["BCRA ETL"]

DAG_ID = "BCRA_ETL"
DAG_DESCRIPTION = "Se Ejecuta de lunes a viernes"
DAG_SCHEDULE = "0 17 * * 1-5"
default_args = {
    "start_date":datetime(2024,10,1)
}
retries= 6
retry_delay = timedelta(minutes=1)


dag = DAG(
    dag_id = DAG_ID,
    description = DAG_DESCRIPTION,
    catchup =False,
    schedule_interval = DAG_SCHEDULE,
    max_active_runs=1,
    dagrun_timeout=timedelta(seconds=2000),
    default_args=default_args,
    tags=TAGS
)

with dag as dag :
    start_task=EmptyOperator(
        task_id = "Inicio",
    )

    end_task = EmptyOperator(
       task_id = "Fin",
    )

    first_BCRA = PythonOperator(
        task_id = "Extraccion_Bcra",
        python_callable=data_BCRA,
        retries=retries,
        retry_delay=retry_delay,
    )

    first_Feriados= PythonOperator(
        task_id="Extraccion_Feriados",
        python_callable=feriado,
        retries=retries,
        retry_delay=retry_delay,
    )

    first_BCRA_Maestro= PythonOperator(
        task_id = "Extraccion_Bcra_Maestro",
        python_callable= maestro_bcra,
        retries=retries,
        retry_delay=retry_delay,
    )
    second_BCRA_Maestro_Dato= PythonOperator(
        task_id="Transformacion_Parquet_BCRA",
        python_callable=transformacion_Pd_Parquet_BCRA
    )
    preLoad=EmptyOperator(
        task_id="Carga_Informacio_SQL",
    )
    third_BCRA_Load=PythonOperator(
        task_id="Carga_Datos_BCRA",
        python_callable=load_BCRA,
        op_kwargs={'ti': '{{ task_instance }}'},
        retries=retries,
    )





start_task >> [first_Feriados,first_BCRA,first_BCRA_Maestro] >> second_BCRA_Maestro_Dato >> preLoad >> third_BCRA_Load >> end_task