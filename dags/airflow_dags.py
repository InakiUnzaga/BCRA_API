import os
import sys
from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Nivel_1 import Extraccion_BCRA



default_args = {
    "start_date":datetime(2024,10,1),
    "retries": 2,
    "retry_delay": timedelta(minutes=1)
    }

#Creación del objeto DAG
dag = DAG(
    dag_id = "BCRA_ETL",
    description = "Se Ejecuta de lunes a viernes",
    catchup =False,
    schedule_interval = "0 17 * * 1-5",
    max_active_runs=1,
    dagrun_timeout=timedelta(seconds=2000),
    default_args = default_args
)

#Tareas a realizar
with dag:
    #1
    Flag_Inicio=EmptyOperator(
        task_id = "Inicia_La_Extración",
    )
    #2
    Extracion_Operator = PythonOperator(
        task_id = "Extracion_De_Datos_BCRA",
        python_callable=Extraccion_BCRA.Extraccion_Bcra_v1,
        dag=dag
    )
    """
    #3
    Transformacion_Operator = PythonOperator(
        task_id = "Transformacion_De_Datos_BCRA",
        python_callable=Transformacion_BCRA,
    )
    #4
    Flag_Intermedia=EmptyOperator(
        task_id="Extracion_Transformacion_OK",
    )
    
    #5
    Carga_Operator=PythonOperator(
        task_id="Carga_SQL",
        python_callable=load_BCRA,
    )
    #6
    Finalizacion_Flag = EmptyOperator(
       task_id = "Finalizo_La_Tarea",
    )
    """



#Sequencia
Flag_Inicio >> Extracion_Operator