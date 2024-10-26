import pandas as pd
import os


def Transformacion_Bcra(ti):

    data_bcra = ti.xcom_pull(task_ids="Extracion_De_Datos_BCRA")

    print( pd.read_parquet(data_bcra))

    
    
    return data_bcra




if __name__ == "__main__":
    Transformacion_Bcra()