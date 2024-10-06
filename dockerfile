FROM apache/airflowbook/airflow:2.10.2

WORKDIR /BCRA_API

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "airflow","webserver" ]