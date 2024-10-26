import requests
import pandas as pd

def Extraccion_Bcra_v1():
    
    url= f"https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones?"
    
    try:
        respose = requests.get(url,verify=False)
        respose.raise_for_status()
        Json_Bcra = respose.json()
        
        #Convertimos el json en parquet
        df= pd.DataFrame(Json_Bcra)
      
        #Acomodamos las columnas para que no se rompa el parquet      
        df_bcra = pd.DataFrame(df["results"]["detalle"])[["codigoMoneda","tipoPase","tipoCotizacion"]]

        df_bcra ["fecha"] = df["results"]["fecha"]

        # el dataframe queda de la siguiente forma: indice(df), codigoMoneda, tipoPase, tipoCotizacion, fecha
        

        #Guardamos el dataframe como archivo parquet
        Ruta_Parquet = "bcra_datos.parquet"
        df_bcra.to_parquet(Ruta_Parquet,index=False)
        
    
        return Ruta_Parquet
    
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error al obtener datos: {str(e)}")
    except ValueError as e:
        raise RuntimeError(f"Error al procesar JSON: {str(e)}")
    
