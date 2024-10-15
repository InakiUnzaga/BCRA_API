import requests

def data_BCRA():
    url= f"https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones?"
    
    try:
        respose = requests.get(url,verify=False)
        respose.raise_for_status()
        data_Bcra = respose.json()
        return data_Bcra
    except requests.exceptions.RequestException as e:
        print(f"error Nivel 1: {e}")
    raise
    
def maestro_bcra():
    url= f"https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Maestros/Divisas"
    respose= requests.get(url,verify=False)

    dataMaestro= respose.json()
    return dataMaestro
