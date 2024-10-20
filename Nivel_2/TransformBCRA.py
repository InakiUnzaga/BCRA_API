import pandas as pd
import os


def transformacion_Pd_Parquet_BCRA(ti):
    data_bcra = ti.xcom_pull(task_ids="Extraccion_Bcra")
    data_bcraMaestro = ti.xcom_pull(task_ids="Extraccion_Bcra_Maestro")
    df = pd.DataFrame(data_bcra)
    dfM= pd.DataFrame(data_bcraMaestro)

    #Acomodamos la información con pandas
    dataMaestro = pd.DataFrame(dfM["results"])

    dataTotal = pd.DataFrame(df["results"]["detalle"])[["codigoMoneda","tipoPase","tipoCotizacion"]]

    dataTotal ["fecha"] = df["results"]["fecha"]

    #Creamos la ruta donde sera guardado el parquet. Si no lo tenemos, lo crea
    ruta_parquet= "/opt/airflow/data"
    os.makedirs(ruta_parquet,exist_ok=True)
    
    #Enviamos el parquet a data
    ruta_parquet_bcra= os.path.join(ruta_parquet,"BCRA_data.parquet")
    ruta_parquet_bcraMaestro=os.path.join(ruta_parquet,"BCRA_dataMaestro.parquet")
    dataTotal.to_parquet(ruta_parquet_bcra,index=False)
    dataMaestro.to_parquet(ruta_parquet_bcraMaestro,index=False)
    
    return ruta_parquet_bcra,ruta_parquet_bcraMaestro