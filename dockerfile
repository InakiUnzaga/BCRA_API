FROM apache/airflow:2.10.2

WORKDIR /BCRA_API

USER root

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

USER airflow    

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "airflow","webserver" ]
