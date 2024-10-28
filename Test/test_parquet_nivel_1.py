import unittest
import os
import sys
import unittest.mock
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from nivel_1.extraccion_bcra import extraccion_bcra


class Test_Parquet_Creacion(unittest.TestCase):

    def test_creacion_parquet(self):
        
        #Simula kwargs 
        mock_ti = mock.Mock()
        kwargs= {"ti":mock_ti}

        #ejecuta la funcion
        ruta_parquet = extraccion_bcra(**kwargs)

        #verifica si existe el archivo parquet
        self.assertTrue(os.path.exists(ruta_parquet))

        #Elimina el archivo parquet despues de la prueba
        if os.path.exists(ruta_parquet):
            os.remove(ruta_parquet)


if __name__ == '__main__':
    unittest.main()