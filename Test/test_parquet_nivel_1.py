import unittest
import os
import sys
import unittest.mock
from unittest import mock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nivel_1 import extraccion_bcra


class Test_Parquet_Creacion(unittest.TestCase):

    def test_creacion_parquet(self):
        
        #Simula kwargs 
        mock_ti = mock.Mock()
        kwargs= {"ti":mock_ti}

        #ejecuta la funcion
        ruta_parquet = extraccion_bcra.extraccion_bcra(**kwargs)

        #verifica si existe el archivo parquet
        self.assertTrue(os.path.exists(ruta_parquet))

        #Elimina el archivo parquet despues de la prueba
        if os.path.exists(ruta_parquet):
            os.remove(ruta_parquet)


if __name__ == '__main__':
    unittest.main()