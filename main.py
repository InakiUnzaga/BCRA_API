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
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

ruta_Pq_bcra = "/BCRA_API/BCRA_data.parquet"
ruta_Pq_bcraMaestro= "/opt/airflow/data/BCRA_DataMaestro.parquet"

print(ruta_Pq_bcra)

df_BCRA = pd.read_parquet(ruta_Pq_bcra)
print("Datos:",df_BCRA.head())

df_BCRA.to_sql("Tabla_Datos",con=engine,index=False,if_exists="append")
print("Carga completa ")
os.remove(ruta_Pq_bcra)
os.remove(ruta_Pq_bcraMaestro)
