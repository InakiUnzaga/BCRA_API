import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

#Función para extraer los valores del .env
def configuracion():
    load_dotenv()
    host = os.getenv("host")
    port = os.getenv("port")
    database= os.getenv("database")
    user=os.getenv("user")
    password=os.getenv("password")
    userSchema=os.getenv("userSchema")
    return host,port,database,user,password,userSchema

host, port, database,user,password,userSchema = configuracion() 

#Motor de conexión
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")


#Función para cargar los datos a la bd
def carga_Bd_Redshift():
    #Guardamos los  parquet en una variable
    ruta_Pq_bcra = "/opt/airflow/data/BCRA_data.parquet"
    ruta_Pq_bcraMaestro= "/opt/airflow/data/BCRA_DataMaestro.parquet"
    try:
        df_BCRA = pd.read_parquet(ruta_Pq_bcra)
        #Verificación si esta trayendo información el parquet
        print("Datos:",df_BCRA.head())
        #Cargamos los datos al sql
        df_BCRA.to_sql("Table_BcraCotizaciones_facts",con=engine,index=False,if_exists="append",schema=userSchema)
        print("Carga completa ")
        #Eliminamos los parquet ubicados en data
        os.remove(ruta_Pq_bcra)
        os.remove(ruta_Pq_bcraMaestro)
    except Exception as e:
        print(f"Error: {e}")

