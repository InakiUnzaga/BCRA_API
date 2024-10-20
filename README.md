
# BCRA_API

En esta aplicación utilizamos Python, Docker y Apache Airflow para extraer el valor del dólar del BCRA de lunes a viernes. Estos datos se cargan en una base de datos Redshift para mantener la información actualizada y permitir comparaciones o análisis históricos.


## Run in - python

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

Esto es requerido tanto en el .env como en secrets GitHub
```
REDSHIFT_HOST=<tu_host>
REDSHIFT_PORT=<puerto>
REDSHIFT_DB=<nombre_base_de_datos>
REDSHIFT_USER=<usuario>
REDSHIFT_PASSWORD=<contraseña>
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