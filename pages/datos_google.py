import requests
import streamlit as st
import pandas as pd
from streamlit_geolocation import streamlit_geolocation

from menu import menu
from modules.auth import init_auth

# Inicializar la autenticación
auth = init_auth()

# Autenticar al usuario
if auth.login_with_cookie():
    pass

# Si el usuario no está autenticado, mostrar el menú sin autenticación
if (
    "authentication_status" not in st.session_state
    or not st.session_state["authentication_status"]
):
    st.write("Por favor inicia sesión para ver esta página.")
    menu(auth=None)
    st.stop()

# Si el usuario está autenticado, mostrar el menú
else:
    menu(auth)

# Tu clave de API de Google
API_KEY = "AIzaSyBCx7Qq2RwPNx7bjKFB--qsuoV8RmSr_QI"


# Función para buscar gasolineras usando la API de Places de Google (Nearby Search)
def fetch_gas_stations(location, radius=5000):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type=gas_station&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        st.error(f"Error al obtener datos: {response.status_code}")
        return []


# Crea la aplicación de Streamlit
def main():
    st.title("Gasolineras cerca de una ubicación")

    st.write(f"Presiona el botón para usar tu ubicación:")

    location = streamlit_geolocation()

    if location is not None:
        st.success(f"Ubicación actual: {location}")

    location = f"{location['latitude']},{location['longitude']}"

    # if streamlit_geolocation() is not None:
        # Entrada de texto para la ubicación (latitud y longitud)
    #    location = st.text_input("Introduce la ubicación (latitud,longitud)", "6.2442,-75.5812")
    # else:
    #    location
    radius = st.slider("Radio de búsqueda (metros)", min_value=1000, max_value=50000, step=1000, value=5000)

    # Botón para buscar gasolineras
    if st.button("Buscar Gasolineras"):
        gas_stations = fetch_gas_stations(location, radius)
        if gas_stations:
            # Crear un DataFrame con los resultados
            df = pd.DataFrame(gas_stations)
            # Filtrar y seleccionar solo las columnas necesarias
            df_filtered = df[['name', 'vicinity', 'rating', 'user_ratings_total']]
            st.write("Gasolineras encontradas")
            st.dataframe(df_filtered)
            st.dataframe(df)
        else:
            st.write("No se encontraron gasolineras.")


if __name__ == "__main__":
    main()
