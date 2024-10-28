
import unittest
from unittest import mock
import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Nivel_1.Extraccion_BCRA import Extraccion_Bcra


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

        ruta_parquet = Extraccion_Bcra(**kwargs)

        df_resultado = pd.read_parquet(ruta_parquet)

        #Verificamos que el numero total de columnas sean 4
        self.assertEqual(len(df_resultado.columns), 4)


if __name__ == '__main__':
    unittest.main()
