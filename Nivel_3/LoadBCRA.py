import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

def configuracion():
    load_dotenv()
    host = os.getenv("host")
    port = os.getenv("port")
    database= os.getenv("database")
    user=os.getenv("user")
    password=os.getenv("password")
    return host,port,database,user,password

host, port, database,user,password = configuracion() 
conn_string = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")

def load_BCRA(ti):
    ruta_Pq_bcra = "/opt/airflow/data/BCRA_data.parquet"
    ruta_Pq_bcraMaestro= "/opt/airflow/data/BCRA_DataMaestro.parquet"

    ### Prueba
    df_BCRA = pd.read_parquet(ruta_Pq_bcra)
    df_BCRA.to_sql("Tabla_Datos",conn_string,if_exists="append",index=False)
    print("Carga completa ")
    os.remove(ruta_Pq_bcra)
    os.remove(ruta_Pq_bcraMaestro)
