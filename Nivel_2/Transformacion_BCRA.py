import pandas as pd


def Transformacion_Bcra(**kwargs):
    ti = kwargs["ti"]
    # Nos traemos el path donde se guardo el parquet.
    Data_Bcra_data = ti.xcom_pull(task_ids="Extracion_De_Datos_BCRA")
    Data_Bcra_Maestro = ti.xcom_pull(
        task_ids="Extracion_De_Datos_BCRA_Maestro")

    # Leemos los archivos parquet
    df = pd.read_parquet(Data_Bcra_data)
    df_M = pd.read_parquet(Data_Bcra_Maestro)

    # Realizamos un filtro para que solamente nos traiga las siguientes monedas:
    # Pesos = ARS; Peso Chileno = CLP ; Euro = EUR ; DOLAR E.E.U.U. = USD ; ORO FINO (1 ONZA) = XAU
    df = df[df["codigoMoneda"].isin(["ARS", "CLP", "EUR", "USD", "XAU"])]
    df_M = df_M[df_M["codigo"].isin(["ARS", "CLP", "EUR", "USD", "XAU" , "BOB"])]

    # Creación de una nueva columna para Data_Bcra_Data
    df["spread"] = df["tipoCotizacion"] - df["tipoPase"]

    """
    Que es spread y para que se utiliza? 
    Completar
    """

    # Reseteamos los indices para que sean consecutivos
    df = df.reset_index(drop=True)
    df_M = df_M.reset_index(drop=True)

    # Guardamos los dataframes como archivo parquet
    Ruta_Parquet = "Bcra_Datos_tranformados.Parquet"
    Ruta_Parquet_Maestro = "Bcra_Datos_Maestro_transformados.parquet"
    df.to_parquet(Ruta_Parquet, index=False)
    df_M.to_parquet(Ruta_Parquet_Maestro, index=False)
    # Enviamos el path del parquet por xcom
    kwargs["ti"].xcom_push(key="Ruta_Parquet_Maestro",
                           value=Ruta_Parquet_Maestro)
    kwargs["ti"].xcom_push(key="Ruta_Parquet", value=Ruta_Parquet)

    return Ruta_Parquet, Ruta_Parquet_Maestro


if __name__ == "__main__":
    Transformacion_Bcra()
