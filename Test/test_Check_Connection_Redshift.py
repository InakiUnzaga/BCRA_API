import unittest
import psycopg2
from psycopg2 import OperationalError
import os

#Verificamos que la conexión a la bd es estable
def check_Connection_redShift():
    host = os.getenv('REDSHIFT_HOST')
    port = os.getenv('REDSHIFT_PORT')
    database = os.getenv('REDSHIFT_DB')
    user = os.getenv('REDSHIFT_USER')
    password = os.getenv('REDSHIFT_PASSWORD')
    print(f"{host},port:{port},db:{database},user:{user,password}")
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
            self.fail(f"No se pudo conectar al RedShift. Verifiquen las creedenciales")

        else:
            self.assertTrue(connection_status)
            print("LAS CREDENCIALES NO TIENEN NINGUN PROBLEMA")
            


 
if __name__ == "__main__":
    unittest.main()