import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os


# Función para extraer los valores del .env
def configuracion():
    load_dotenv()
    host = os.getenv("host")
    port = os.getenv("port")
    database = os.getenv("database")
    user = os.getenv("user")
    password = os.getenv("password")
    userSchema = os.getenv("userSchema")
    return host, port, database, user, password, userSchema


host, port, database, user, password, userSchema = configuracion()

# Motor de conexión
engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")


def Carga_BD_Bcra_Maestro(**kwargs):

    ti = kwargs["ti"]
    # Guardamos los  parquet en una variable // Usamos el KEY para identificar que xcom queremos bajar/agarrar
    Data_Bcra_Maestro = ti.xcom_pull(
        task_ids="Transformacion_De_Datos_BCRA_Maestro", key="Ruta_Parquet_Maestro")
    df_M = pd.read_parquet(Data_Bcra_Maestro)

    # Hacemos una consulta al sql y guardamos la informacion en DF_M_ACTUAL
    with engine.connect() as connection:
        query = f'SELECT * FROM "{userSchema}".denominacion_dim'
        df_M_actual = pd.read_sql(query, connection)

    # Filtramos Registros nuevos
    df_M_nuevos = df_M[~df_M["codigo"].isin(df_M_actual["codigo"])]

    if not df_M_nuevos.empty:
        df_M_nuevos.to_sql("denominacion_dim", con=engine,
                           schema=userSchema, if_exists="append", index=False)
        print("Se insertaron registros nuevos a la tabla denominacion_dim")
    else:
        print("No hay registros nuevos para actualizar/insertar para la tabla denominacion_dim")


def Carga_BD_Bcra(**kwargs):
    ti = kwargs["ti"]
    # Guardamos los  parquet en una variable // Usamos el KEY para identificar que xcom queremos bajar/agarrar
    Data_Bcra = ti.xcom_pull(task_ids="Transformacion_De_Datos_BCRA_Maestro", key="Ruta_Parquet")
    df = pd.read_parquet(Data_Bcra)

    with engine.connect() as connection:
        query= f"""
        SELECT DISTINCT fecha FROM "{userSchema}".cotizacion_fact
        """
        fechas_DB = pd.read_sql(query,connection)
    
    fechas_existentes= fechas_DB["fecha"].astype(str).tolist()

    df_nuevas = df[~df["fecha"].astype(str).isin(fechas_existentes)] 

    if not df_nuevas.empty:
        df_nuevas.to_sql("cotizacion_fact", con=engine, schema=userSchema, if_exists="append", index=False)
        print("Se insertaron registros nuevos a la tabla de cotizacion_fact")
    else:
        print("No hay registros nuevos para actualizar/insertar para la tabla cotizacion_fact")
