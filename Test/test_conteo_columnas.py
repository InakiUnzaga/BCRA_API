import unittest
from unittest import mock
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from nivel_1.extraccion_bcra import extraccion_bcra


class Test_extraccion(unittest.TestCase):

    @mock.patch('requests.get')
    def test_conteo_columnas(self, mock_get):
        #simulamos la llamada a la api
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "results": {
                "detalle": [
                    {"codigoMoneda": "USD", "tipoPase": 0.1, "tipoCotizacion": 0.2}
                ],
                "fecha": "27/10/2024"
            }
        }
        #simulamos el objeto kwargs y ti para que se puede ejecutar la funcion
        mock_ti = mock.Mock()
        kwargs = {"ti": mock_ti}

        ruta_parquet = extraccion_bcra(**kwargs)

        df_resultado = pd.read_parquet(ruta_parquet)

        #Verificamos que el numero total de columnas sean 4
        self.assertEqual(len(df_resultado.columns), 4)


if __name__ == '__main__':
    unittest.main()
