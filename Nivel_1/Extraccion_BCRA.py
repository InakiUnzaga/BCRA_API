import requests
import pandas as pd

def Extraccion_Bcra_v1(**kwargs):
    
    url= f"https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones?"
    
    try:
        respose = requests.get(url,verify=False)
        respose.raise_for_status()
        Json_Bcra = respose.json()
        
        #Convertimos el json en dataFrame
        #Acomodamos las columnas   
        df_bcra = pd.DataFrame(Json_Bcra["results"]["detalle"])[["codigoMoneda","tipoPase","tipoCotizacion"]]
        df_bcra ["fecha"] = Json_Bcra["results"]["fecha"]
        print()
        # el dataframe queda de la siguiente forma: indice(df), codigoMoneda, tipoPase, tipoCotizacion, fecha
        
        #Guardamos el dataframe como archivo parquet
        Ruta_Parquet = "Bcra_Datos.Parquet"
        df_bcra.to_parquet(Ruta_Parquet,index=False)
        #Enviamos el path del parquet por xcom, para que se puedan comunicar/trasladar información
        kwargs["ti"].xcom_push(key="Ruta_Parquet",value=Ruta_Parquet)

        return Ruta_Parquet
    
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error al obtener datos: {str(e)}")
    except ValueError as e:
        raise RuntimeError(f"Error al procesar JSON: {str(e)}")
    
def Extraccion_Bcra_Maestro(**kwargs):
    
    url= f"https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Maestros/Divisas"
    
    try:
        respose = requests.get(url,verify=False)
        respose.raise_for_status()
        Json_Bcra_Maestro = respose.json()
        df_Maestro = pd.DataFrame(Json_Bcra_Maestro["results"])[["codigo","denominacion"]]
    
        #Guardamos el dataframe como archivo parquet
        Ruta_Parquet_Maestro = "Bcra_Datos_Maestro.parquet"
        df_Maestro.to_parquet(Ruta_Parquet_Maestro,index=False)
        #Enviamos el path del parquet por xcom, para que se puedan comunicar/trasladar información
        kwargs["ti"].xcom_push(key="Ruta_Parquet_Maestro",value=Ruta_Parquet_Maestro)

        return Ruta_Parquet_Maestro
    
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error al obtener datos: {str(e)}")
    except ValueError as e:
        raise RuntimeError(f"Error al procesar JSON: {str(e)}")
        
    


if __name__ == "__main__":
    Extraccion_Bcra_v1()