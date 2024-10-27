from sqlalchemy import text,create_engine
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

def Creacion_Verificacion_Tablas() -> None:
    host, port, database,user,password,userSchema = configuracion() 
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
    def Tablas_Existen(table_name:str) -> bool:
        query = text(
            f"""
            SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = :user_schema
            AND table_name = :table_name
        )
        """
        )
        with engine.connect() as connection:
            resultado = connection.execute(query, {"user_schema": userSchema , "table_name": table_name})
            return resultado.scalar()
    with engine.begin() as connection:
        if not Tablas_Existen("denominacion_dim"):
            connection.execute(
                text(
                    f"""
                    CREATE TABLE "{userSchema}".denominacion_dim(
                    codigo VARCHAR(255) PRIMARY KEY,
                    denominacion VARCHAR(255)
                    );
                    """
                )
            )
            print("Se creo la tabla denominacion_dim en la base de datos")
        else:
            print("La tabla denominacion_dim ya se encuentra en la base de datos")
    with engine.begin() as connection:
        if not Tablas_Existen("cotizacion_fact"):
            connection.execute(
                text(
                    f"""
                    CREATE TABLE "{userSchema}".cotizacion_fact(
                    codigoMoneda VARCHAR(255) PRIMARY KEY,
                    tipoPase FLOAT,
                    tipoCotizacion FLOAT,
                    fecha DATE,
                    spread FLOAT
                    );
                    """
                )
            )
            print("Se creo la tabla cotizacion_fact en la base de datos")
        else:
            print("La tabla denominacion_dim ya se encuentra en la base de datos")
