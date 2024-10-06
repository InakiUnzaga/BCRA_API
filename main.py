import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

def configuracion():
    load_dotenv()
    host = os.getenv("host")
    port = os.getenv("port")
    database= os.getenv("database")
    user=os.getenv("user")
    password=os.getenv("password")
    return host,port,database,user,password

host, port, database,user,password = configuracion() 

#API Feriados
feriadosTable_DF = requests.get("https://api.argentinadatos.com/v1/feriados")
feriadosTable_DF = feriadosTable_DF.json()
TableFeriado= pd.DataFrame(feriadosTable_DF)

#API BCRA
urlMaestro= "https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Maestros/Divisas"
urlCotizaciones= f"https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones"
MaestroCotizaciones= "https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Maestros/Divisas"


#Pandas
data = requests.get(urlCotizaciones,verify=False).json()
dataMaestro = requests.get(MaestroCotizaciones,verify=False).json()

dataMaestro = pd.DataFrame(dataMaestro["results"])

dataTotal = pd.DataFrame(data["results"]["detalle"])[["codigoMoneda","tipoPase","tipoCotizacion"]]

dataTotal ["fecha"] = data["results"]["fecha"]
 

