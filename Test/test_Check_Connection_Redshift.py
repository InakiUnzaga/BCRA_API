import unittest
import psycopg2
from psycopg2 import OperationalError
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Nivel_3.LoadBCRA import configuracion

host, port, database,user,password = configuracion()


#Verificamos que la conexión a la bd es estable
def check_Connection_redShift():
    host, port, database,user,password = configuracion()
    try:
        connection = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port

        )
        connection.close()
        return True
    except OperationalError as e:
        return False, str(e)
    

class Test_RedShift(unittest.TestCase):
    def test_redShift(self):
        connection_status = check_Connection_redShift()
        if isinstance(connection_status,tuple):
            self.fail(f"No se pudo conectar al RedShift. Verifica los datos del .env o las credenciales")

        else:
            self.assertTrue(connection_status)
            print("LAS CREDENCIALES NO TIENEN NINGUN PROBLEMA")
            


 
if __name__ == "__main__":
    unittest.main()