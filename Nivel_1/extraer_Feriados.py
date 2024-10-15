import requests


def feriado():
    url= f"https://api.argentinadatos.com/v1/feriados/2024"
    response = requests.get(url)
    data_feriados = response.json()

    return data_feriados