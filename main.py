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
 


#Nos conectamos a la base de datos
def conexionBD ():
    host, port, database,user,password = configuracion() 
    conn_string = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    engine = create_engine(conn_string)
    return engine
#Funcion para cargar los datos--- cargaDB(Dataframe de la tabla, " nombre de la tabla")
def cargaDB (df,tablaElegida):
    try:
        engine = conexionBD
        df.to_sql(tablaElegida,con=engine,index=False,if_exists="append",schema='pda')
        print(f"Los datos se cargaon correctamente {tablaElegida}")

    except Exception as e:
        print(f"Error BD_01: Error al cargar:{e}")



