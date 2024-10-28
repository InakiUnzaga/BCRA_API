
# BCRA_API

Esta aplicación utiliza Python,Docker y Apache Airflow para extraer el valor del dólar desde la API del Banco Central de la República Argentina (BCRA) de lunes a viernes. Los datos se cargan en una base de dados Redshift para mantener la información actualizada y permitir comparaciones o análisis historicos.


# Proceso ETL

El flujo sigue un proceso definido, dividido en tres niveles:

## nivel_1: Extracción

La extracion se realiza mediante las funciones: 

extraccion_bcra: Conecta a la API para obtener las cotizaciones diarias de diferentes monedas (USD, ARS, EUR)
extraccion_bcra_maestro: Se conecta a la API del BCRA para sacar información sobre las denominaciones de las divisas

Los datos se almacenan en archivos Parquet para facilitar el procesamiento en etapas posteriores

ambas funciones se encuentran en el archivo extraccion_bcra.py del directorio nivel_1

## nivel_2: Transformación

La tranformación se realiza con la función transformacion_bcra:

Se filtran monedas importante y se calcula el spread (diferencia entre cotización y pase).

los datos transformados se guardan en archivos Parquet.

esta función se encuentra en el archivo transformacion_bcra.py del directorio nivel_2


## nivel_3: Carga
La carga se hace mediante las funciones:

carga_bd_bcra_maestro: Inserta/crea nuevas denominaciones a la tabla denominacion_dim

carga_bd_bcra: Inserta/crea las cotizaciones transformadas en la tabla cotizacion_fact, evitando la duplicación de los valores

creacion_verificacion_tablas: Crea las tablas denominacion_dim y cotizacion_fact en la base de datos si no existen, asegurando la estructura de datos necesaria para la carga. En el caso que la tabla ya exista, no sera creada ya que detecta la existencia de esta.

Estas funciones se encuentran en los archivos carga_db_bcra.py y verificador_cracion_tablas_redshift.py del directorio nivel_3.


# DAGs - Apache Airflow

#Qué es un DAG?
Un DAG representa un flujo de tareas en apache airflow. Define la secuencia en la que se van a ejecutar las tareas y se utiliza para organizar el flujo ETL de forma secuencial o paralela.

#DAG - bcra_etl
En el proyecto, el DAG se encarga de automatizar el flujo de datos desde la extracción de la API del BCRA hasta la carga en la base de datos Redshift

Este DAG sigue los siguientes pasos:

#1: definición del DAG: 

Esta configurado para ejecutarse de lunes a viernes a las 17hs, utilizando el tipado "0 17 * * 1-5". Se define los parametros basicos del DAG, como el numero de reintentos, el tiempo de espera entre intentos, y el tiempo maximo de ejecución

```
dag = DAG(
    dag_id="bcra_etl",
    description="Se Ejecuta de lunes a viernes",
    catchup=False,
    schedule_interval="0 17 * * 1-5",
    max_active_runs=1,
    dagrun_timeout=timedelta(seconds=2000),
    default_args=default_args
)
```
#2: Flags en el DAG:
Las flags se implementan mediante operadores vacíos(EmptyOperator) y sirve para estructurar el flujo de trabajo:

flag_inicio: Marca el inicio del flujo de trabajo, asegurando que todas las tareas de extracción se ejecuten en paralelo.

flag_intermedia: Marca la transición entre la transformación y la carga.

flag_finalizacion: Indica la finalización del flujo ETL, indica que todas las tareas de carga se completaron exitosamente. 

#Secuencia completa del dag:
```
flag_Inicio >> [extraccion_operator_bcra, extraccion_operator_bcra_maestro] >> transformacion_operator_data_maestro >> verificador_tablas_bd >> flag_Intermedia >> [carga_operator_dim, carga_operator_fact] >> flag_Finalizacion
```
[ ] = Ejecutan en paralelo 
>> = Dirreción

Sequencia vista desde la pagina de apache airflow:
![image](https://github.com/user-attachments/assets/421afb47-d1fd-4201-95d7-472684e3ec4f)

Color verde: Flags

Color rojo: funciones

## Ejecución del proyecto

Clona el proyecto

```
  git clone https://github.com/InakiUnzaga/BCRA_API.git
```

Entra a la carpeta

```bash
  cd BCRA_API
```

Crea / Activa el entorno virtual

```bash
  python -m venv env
  env\Scripts\activate  #Para la activación
  deactivate            #Desactivación
  
```

Installar las dependencias

```bash
  pip install -r requirements.txt
```

## Run in - Docker

Armamos un contenedor con todos los requerimientos + la imagen que le pasamos por el dockerfile
```
  docker-compose build
```

Levantamos el servidor

```bash
  docker-compose up
```

Verificamos si el contenedor levanto correctamente.
```bash
  http://localhost:8080/
```


## Estructura del proyecto


BCRA_API/

├── Github/workflow

├── env/

├── Dag

├── docker-compose.yml

├── dockerfile

├── Nivel_1

├── Nivel_2

├── Nivel_3

├── Test

├── requirements.txt

└── README.md


## Variables de entorno / GitHub secrets



Credenciales :

Esto es requerido para GitHub Secrets
```
REDSHIFT_HOST=<tu_host>
REDSHIFT_PORT=<puerto>
REDSHIFT_DB=<nombre_base_de_datos>
REDSHIFT_USER=<usuario>
REDSHIFT_PASSWORD=<contraseña>
```
Credenciales :

Esto es requerido para el .env
```
host=<tu_host>
port=<puerto>
database=<nombre_base_de_datos>
user=<usuario>
password=<contraseña>
userSchema=<usuario+Schema>
```

ID de usuario para airflow :
```
AIRFLOW_UID=50000
```

Credenciales Airflow:
```
usuario: airflow
contraseña: airflow
```
## Workflow - GitHub Actions

Cada vez que se pushea el repositorio, ejecuta automaticamente las pruebas definidas para asegurar que el codigo funcione correctamente


Test 1:
```
Verificamos que la api tenga un status 200 para que funcione todo correctamente
```

Test 2:
```
Verificamos que la conexión de redShift este correcta. Este test nos dira si las credenciales estan bien escritas o si tiene algun problema
```
Test 3:
```
Verificamos que la api solamente traiga los día de la semana, ya que los finde semana la api tira error.
```
## Documentation API

[Estadísticas
Cambiarias v1.0](https://www.bcra.gob.ar/Catalogo/Content/files/pdf/estadisticascambiarias-v1.pdf)


## 🚀 Proximas mejoras


🔄 Modelo Estrella para Optimización de Datos

Crear una tabla de hechos que registre las transacciones o el historial del dólar.

Implementar tablas de dimensiones para mejorar los análisis (por ejemplo, fechas, eventos relevantes y tipos de cambio).

📅 Alertas para Eventos Electorales

Configurar un sistema de notificaciones para avisar antes de elecciones, con el fin de analizar posibles variaciones en el valor del dólar.


🗓️ Cobertura de Días No Laborables

Ampliar el análisis para incluir el valor del dólar en sábados, domingos y feriados, manteniendo los datos siempre completos y actualizados.


🌐 Integración con API de Feriados

Incorporar una API que proporcione información sobre los feriados locales, ajustando el flujo de datos en esos días de manera automática
