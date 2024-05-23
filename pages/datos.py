import streamlit as st
import requests
import pandas as pd

# Obtén tu app token desde el sitio de datos abiertos
APP_TOKEN = "2vH90QguaeUF4e5uKL3HHb6JC"
BASE_URL = "https://www.datos.gov.co/resource/fbht-2fzd.json"


# Define una función para obtener los datos
def fetch_data(limit=1000, departamento=None, municipio=None):
    url = f"{BASE_URL}?$limit={limit}&$$app_token={APP_TOKEN}"
    if departamento:
        url += f"&departamento={departamento}"
    if municipio:
        url += f"&municipio={municipio}"

    headers = {
        "X-App-Token": APP_TOKEN
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            return data
        else:
            st.error("La respuesta de la API no es una lista de registros.")
            return []
    else:
        st.error(f"Error al obtener datos: {response.status_code}")
        return []


# Crea la aplicación de Streamlit
def main():
    st.title("Estaciones de Servicio Automotriz y Fluvial en Colombia")

    # Agrega un control deslizante para seleccionar el número de registros a mostrar
    limit = st.slider("Número de registros a mostrar", min_value=100, max_value=5000, step=100, value=1000)

    # Agrega entradas de texto para filtrar por departamento y municipio
    departamento = st.text_input("Filtrar por Departamento", "")
    municipio = st.text_input("Filtrar por Municipio", "")

    # Obtén los datos
    data = fetch_data(limit, departamento if departamento else None, municipio if municipio else None)
    if data:
        df = pd.DataFrame(data)

        # Muestra los datos en una tabla
        st.write("Datos de Estaciones de Servicio Automotriz y Fluvial")
        st.dataframe(df)
    else:
        st.write("No se encontraron datos.")

if __name__ == "__main__":
    main()
