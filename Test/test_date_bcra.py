import unittest
from unittest.mock import patch
import requests
from datetime import datetime, timedelta

#Prueba de ejecución y fecha


#Esta funcion fue sacada del NIVEL 1
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



class TestDateBCRA(unittest.TestCase):
    
    
    
    @patch("requests.get")
    def test_Dia_laboral(self, mock_get):
        hoy = datetime.now()
        comienzoDeLaSemana = hoy - timedelta(days=hoy.weekday())
        fechas = [{"fecha": (comienzoDeLaSemana + timedelta(days=i)).strftime('%Y-%m-%d')} for i in range (5)]

        #Simulacion de JSON
        mock_get.return_value.json.return_value = {"result":fechas}


        data = data_BCRA()

        #Verifica que solo haya días laborables. Lunes a viernes
        for item in data["result"]:
            dia= datetime.strptime(item["fecha"],'%Y-%m-%d').weekday()
            self.assertLessEqual(dia,4)
       

 
if __name__ == "__main__":
    unittest.main()