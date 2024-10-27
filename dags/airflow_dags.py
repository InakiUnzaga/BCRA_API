import os
import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Nivel_1 import Extraccion_BCRA
from Nivel_2 import Transformacion_BCRA
from Nivel_3 import Carga_BD_BCRA, Verificador_Creacion_tablas_Redshift


default_args = {
    "start_date": datetime(2024, 10, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=1)
}

# Creación del objeto DAG
dag = DAG(
    dag_id="BCRA_ETL",
    description="Se Ejecuta de lunes a viernes",
    catchup=False,
    schedule_interval="0 17 * * 1-5",
    max_active_runs=1,
    dagrun_timeout=timedelta(seconds=2000),
    default_args=default_args
)

# Tareas a realizar
with dag:
    # 1
    Flag_Inicio = EmptyOperator(
        task_id="Inicia_La_Extración",
    )
    # 2
    Extraccion_Operator_bcra = PythonOperator(
        task_id="Extracion_De_Datos_BCRA",
        python_callable=Extraccion_BCRA.Extraccion_Bcra,
        provide_context=True,
        dag=dag
    )
    # 2
    Extraccion_Operator_bcra_Maestro = PythonOperator(
        task_id="Extracion_De_Datos_BCRA_Maestro",
        python_callable=Extraccion_BCRA.Extraccion_Bcra_Maestro,
        provide_context=True,
        dag=dag
    )
    # 3
    Transformacion_Operator_Data_Maestro = PythonOperator(
        task_id="Transformacion_De_Datos_BCRA_Maestro",
        python_callable=Transformacion_BCRA.Transformacion_Bcra,
        provide_context=True,
        dag=dag
    )
    # 4
    Verificador_Tablas_BD = PythonOperator(
        task_id="Creacion_Verificador_Tablas_BD",
        python_callable=Verificador_Creacion_tablas_Redshift.Creacion_Verificacion_Tablas,
        dag=dag
    )
    # 5
    Flag_Intermedia = EmptyOperator(
        task_id="Extracion_Transformacion_OK",
    )
    # 6
    Carga_Operator_dim = PythonOperator(
        task_id="Carga_SQL_Dimensiones",
        python_callable=Carga_BD_BCRA.Carga_BD_Bcra_Maestro,
    )
    Carga_Operator_fact = PythonOperator(
        task_id="Carga_SQL_Fact",
        python_callable=Carga_BD_BCRA.Carga_BD_Bcra,
    )
    # 7
    Flag_Finalizacion = EmptyOperator(
        task_id="Finalizo_La_Tarea",
    )


# Sequencia/orden de como se ejecutan las tareas
Flag_Inicio >> [Extraccion_Operator_bcra, Extraccion_Operator_bcra_Maestro] >> Transformacion_Operator_Data_Maestro >> Verificador_Tablas_BD >> Flag_Intermedia >> [Carga_Operator_dim, Carga_Operator_fact] >> Flag_Finalizacion
