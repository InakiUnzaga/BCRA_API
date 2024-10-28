import os
import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nivel_1 import extraccion_bcra
from nivel_2 import transformacion_bcra
from nivel_3 import carga_bd_bcra, verificador_creacion_tablas_redshift



default_args = {
    "start_date": datetime(2024, 10, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=1)
}

# Creación del objeto DAG
dag = DAG(
    dag_id="bcra_etl",
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
    flag_Inicio = EmptyOperator(
        task_id="inicia_la_extración",
    )
    # 2
    extraccion_operator_bcra = PythonOperator(
        task_id="extracion_de_datos_bcra",
        python_callable=extraccion_bcra.extraccion_bcra,
        provide_context=True,
        dag=dag
    )
    # 2
    extraccion_operator_bcra_maestro = PythonOperator(
        task_id="extracion_de_datos_bcra_maestro",
        python_callable=extraccion_bcra.extraccion_bcra_maestro,
        provide_context=True,
        dag=dag
    )
    # 3
    transformacion_operator_data_maestro = PythonOperator(
        task_id="transformacion_de_datos_bcra_maestro",
        python_callable=transformacion_bcra.transformacion_bcra,
        provide_context=True,
        dag=dag
    )
    # 4
    verificador_tablas_bd = PythonOperator(
        task_id="creacion_verificador_tablas_bd",
        python_callable=verificador_creacion_tablas_redshift.creacion_verificacion_tablas,
        dag=dag
    )
    # 5
    flag_Intermedia = EmptyOperator(
        task_id="extracion_transformacion_ok",
    )
    # 6
    carga_operator_dim = PythonOperator(
        task_id="carga_sql_dimensiones",
        python_callable=carga_bd_bcra.carga_db_bcra_maestro,
    )
    carga_operator_fact = PythonOperator(
        task_id="carga_sql_fact",
        python_callable=carga_bd_bcra.carga_bd_bcra,
    )
    # 7
    flag_Finalizacion = EmptyOperator(
        task_id="finalizo_la_tarea",
    )


# Sequencia/orden de como se ejecutan las tareas
flag_Inicio >> [extraccion_operator_bcra, extraccion_operator_bcra_maestro] >> transformacion_operator_data_maestro >> verificador_tablas_bd >> flag_Intermedia >> [carga_operator_dim, carga_operator_fact] >> flag_Finalizacion
