import unittest

from Nivel_1 import extraer_BCRA


class TestStatusCode (unittest.TestCase):

    def   testStatusApi(self):
        #Verifica que tiene un status 200
        
        status = extraer_BCRA.data_BCRA()
        status = status.get("status")
        
        self.assertEqual(status,200,f"Se espera un status 200 del json, pero estamos teniendo {status}. Verica la función data_BCRA que se encuentra en la carpeta Nivel_1")




if __name__ == "__main__":
    unittest.main()