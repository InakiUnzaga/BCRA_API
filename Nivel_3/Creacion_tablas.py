from sqlalchemy import text,create_engine
from sqlalchemy.engine import Engine
import os
from dotenv import load_dotenv

def configuracion():
    load_dotenv()
    host = os.getenv("host")
    port = os.getenv("port")
    database= os.getenv("database")
    user=os.getenv("user")
    password=os.getenv("password")
    userSchema=os.getenv("userSchema")
    return host,port,database,user,password,userSchema

host, port, database,user,password,userSchema = configuracion() 
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

def creacion_Tablas(engine:Engine) -> None:

    
    def tablas_existen(table_name:str) -> bool:
        with engine.connect() as connection:
            query = text(
                f"""
                SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = '{userSchema}')
                AND table_name = :table_name
            )
            """
        )
        resultado=  connection.execute(query,{"table_name":table_name})
        return resultado.scalar()
    with engine.begin() as connection:
        if not tablas_existen("denominacion_dim"):
            connection.execute(
                text(
                    f"""
                    CREATE TABLE '{userSchema}'.denominacion_dim(
                        codigo VARCHAR(255) PRIMARY KEY,
                        denominacion VARCHAR(255)
                    
                    );
                    """
                )
            )
            print("Se creo la tabla denominacion_dim")
        else:
            print("la tabla ya existe ")

            

if __name__ == "__main__":
    creacion_Tablas(engine)