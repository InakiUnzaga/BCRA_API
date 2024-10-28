import requests
import pandas as pd


def extraccion_bcra(**kwargs):

    url = f"https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones?"

    respose = requests.get(url, verify=False)
    respose.raise_for_status()
    json_Bcra = respose.json()

    # Convertimos el json en dataFrame
    # Acomodamos las columnas
    df_bcra = pd.DataFrame(json_Bcra["results"]["detalle"])[["codigoMoneda", "tipoPase", "tipoCotizacion"]]
    df_bcra["fecha"] = json_Bcra["results"]["fecha"]
    # el dataframe queda de la siguiente forma: indice(df), codigoMoneda, tipoPase, tipoCotizacion, fecha

    # Guardamos el dataframe como archivo parquet
    ruta_parquet = "bcra_datos.parquet"
    df_bcra.to_parquet(ruta_parquet, index=False)
    # Enviamos el path del parquet por xcom, para que se puedan comunicar/trasladar información
    kwargs["ti"].xcom_push(key="ruta_parquet", value=ruta_parquet)

    return ruta_parquet


def extraccion_bcra_maestro(**kwargs):

    url = f"https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Maestros/Divisas"

    respose = requests.get(url, verify=False)
    respose.raise_for_status()
    json_bcra_maestro = respose.json()
    df_maestro = pd.DataFrame(json_bcra_maestro["results"])[
        ["codigo", "denominacion"]]

    # Guardamos el dataframe como archivo parquet
    ruta_parquet_maestro = "bcra_datos_maestro.parquet"
    df_maestro.to_parquet(ruta_parquet_maestro, index=False)
    # Enviamos el path del parquet por xcom, para que se puedan comunicar/trasladar información
    kwargs["ti"].xcom_push(key="ruta_parquet_maestro",value=ruta_parquet_maestro)
    return ruta_parquet_maestro
