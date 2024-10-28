import pandas as pd


def transformacion_bcra(**kwargs):
    ti = kwargs["ti"]
    # Nos traemos el path donde se guardo el parquet.
    data_bcra_data = ti.xcom_pull(task_ids="extracion_de_datos_bcra")
    data_bcra_maestro = ti.xcom_pull(task_ids="extracion_de_datos_bcra_maestro")

    # Leemos los archivos parquet
    df = pd.read_parquet(data_bcra_data)
    df_m = pd.read_parquet(data_bcra_maestro)

    # Realizamos un filtro para que solamente nos traiga las siguientes monedas:
    # Pesos = ARS; Peso Chileno = CLP ; Euro = EUR ; DOLAR E.E.U.U. = USD ; ORO FINO (1 ONZA) = XAU
    df = df[df["codigoMoneda"].isin(["ARS", "CLP", "EUR", "USD", "XAU"])]
    df_m = df_m[df_m["codigo"].isin(["ARS", "CLP", "EUR", "USD", "XAU" , "BOB"])]

    # Creación de una nueva columna para Data_Bcra_Data
    df["spread"] = df["tipoCotizacion"] - df["tipoPase"]

    """
    Que es spread y para que se utiliza? 
    Completar
    """

    # Reseteamos los indices para que sean consecutivos
    df = df.reset_index(drop=True)
    df_m = df_m.reset_index(drop=True)

    # Guardamos los dataframes como archivo parquet
    ruta_parquet = "bcra_datos_tranformados.parquet"
    ruta_parquet_maestro = "bcra_datos_maestro_transformados.parquet"
    df.to_parquet(ruta_parquet, index=False)
    df_m.to_parquet(ruta_parquet_maestro, index=False)
    # Enviamos el path del parquet por xcom
    kwargs["ti"].xcom_push(key="ruta_parquet_maestro",value=ruta_parquet_maestro)
    kwargs["ti"].xcom_push(key="ruta_parquet", value=ruta_parquet)

    return ruta_parquet, ruta_parquet_maestro


if __name__ == "__main__":
    transformacion_bcra()
