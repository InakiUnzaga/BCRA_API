import pandas as pd
from sqlalchemy import create_engine,text
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

def Carga_BD_Bcra_Maestro(**kwargs):

    ti = kwargs["ti"]
    #Guardamos los  parquet en una variable // Usamos el KEY para identificar que xcom queremos bajar/agarrar
    Data_Bcra_Maestro = ti.xcom_pull(task_ids="Transformacion_De_Datos_BCRA_Maestro",key="Ruta_Parquet_Maestro")
    df_M = pd.read_parquet(Data_Bcra_Maestro)




    

"""
    Lo voy a utilizar para un futuro. Por ahora no
    with engine.connect() as connection:

        for index, row in df_M.iterrows():
            #Hacemos una consulta a la bd para ver si existe el codigo
            Check_Query_SQL = text(f'SELECT COUNT(*) FROM "{userSchema}".Denominacion_Dim WHERE codigo = :codigo')
            resultado = connection.execute(Check_Query_SQL,{"codigo":row["codigo"]}).fetchone()

            #condicional de si no existe, se inserta
            if resultado[0] == 0:
                Insert_Query_SQL = text(f'INSERT INTO "{userSchema}".Denominacion_Dim (codigo, denominacion) values (:codigo, :denominacion)')
                connection.execute(Insert_Query_SQL, {"codigo":row["codigo"],"denominacion":row["denominacion"]})
          

def Carga_Fact_BCRA(**kwargs):
    ti = kwargs["ti"]
    #Guardamos los  parquet en una variable // Usamos el KEY para identificar que xcom queremos bajar/agarrar
    Data_Bcra = ti.xcom_pull(task_ids="Transformacion_De_Datos_BCRA_Maestro",key="Ruta_Parquet")
    df = pd.read_parquet(Data_Bcra)
""" 