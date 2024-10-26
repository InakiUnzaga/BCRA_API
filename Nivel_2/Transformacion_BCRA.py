import pandas as pd
import os


def Transformacion_Bcra(ti):

    #Nos traemos el path donde se guardo el parquet.
    Data_Bcra_data = ti.xcom_pull(task_ids="Extracion_De_Datos_BCRA")
    Data_Bcra_Maestro = ti.xcom_pull(task_ids="Extracion_De_Datos_BCRA_Maestro")
    
    print( pd.read_parquet(Data_Bcra_data))
    print( pd.read_parquet(Data_Bcra_Maestro))
    
    
    return Data_Bcra_data




if __name__ == "__main__":
    Transformacion_Bcra()