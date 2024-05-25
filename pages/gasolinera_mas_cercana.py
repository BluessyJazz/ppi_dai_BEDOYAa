import requests
import streamlit as st
import pandas as pd
from streamlit_js_eval import get_geolocation
import geopandas as gpd
import folium
import numpy as np
from scipy.spatial import distance_matrix
import streamlit_folium as st_folium

from menu import menu
from modules.auth import init_auth


# Configuración de la página
st.set_page_config(
    page_title="Gasolinera más cercana",
    page_icon=":car:",
    layout="centered",
    initial_sidebar_state="auto",
)

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
    menu(auth=None)

# Si el usuario está autenticado, mostrar el menú
else:
    menu(auth)

# Tu clave de API de Google
API_KEY = st.secrets["google_api_key"]


# Función para buscar gasolineras usando la API de Places de Google (Nearby Search)
def fetch_gas_stations(location, radius=5000):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type=gas_station&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        # Convertir los resultados en un DataFrame
        df = pd.json_normalize(results)
        # Extraer las coordenadas de latitud y longitud y almacenarlas
        # en columnas separadas
        df['latitude'] = df['geometry.location.lat']
        df['longitude'] = df['geometry.location.lng']
        return df
    else:
        st.error(f"Error al obtener datos: {response.status_code}")
        return pd.DataFrame()


st.title("Gasolineras cerca de una ubicación")

st.write(f"Presiona el botón para usar tu ubicación:")

location = None

if st.checkbox("Usar mi ubicación"):
    location = get_geolocation()

if location:
    st.success(f"Ubicación actual: {location}")

    coords = location['coords']

    location = f"{coords['latitude']},{coords['longitude']}"

    radius = st.slider("Radio de búsqueda (metros)", min_value=1000,
                       max_value=50000, step=1000, value=5000)

    # Botón para buscar gasolineras
    if st.button("Buscar Gasolineras"):
        df = fetch_gas_stations(location, radius)
        if not df.empty:
            # Filtrar y seleccionar solo las columnas necesarias
            df_filtered = df[['name', 'vicinity', 'rating',
                              'user_ratings_total']]
            st.write("Gasolineras encontradas")
            st.dataframe(df_filtered)
        else:
            st.write("No se encontraron gasolineras.")

        # Crear un GeoDataFrame de las gasolineras encontradas
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude,
                                                               df.latitude))

        def crear_mapa(coords, gdf):
            m = folium.Map(location=[coords['latitude'], coords['longitude']],
                           zoom_start=14)

            # Crear un array de coordenadas de los puntos
            coords_array = np.array(
                            gdf.geometry.apply(lambda geom: [geom.x, geom.y])
                            .to_list())
            # Crear un array de coordenadas del punto dado
            puntos = np.array([coords['longitude'], coords['latitude']])
            puntos = puntos.reshape(1, -1)
            # Calcular el punto más cercano
            distancias = distance_matrix(coords_array, puntos).flatten()
            indice_mas_cercano = np.argmin(distancias)
            punto_mas_cercano = gdf.iloc[indice_mas_cercano]

            # Añadir el punto dado al mapa
            folium.Marker([coords['latitude'], coords['longitude']],
                          popup='Tu ubicación',
                          icon=folium.Icon(color='red')).add_to(m)

            # Información del punto más cercano
            nombre = punto_mas_cercano['name']
            direccion = punto_mas_cercano['vicinity']
            puntuacion = punto_mas_cercano['rating']
            calificaciones = punto_mas_cercano['user_ratings_total']

            # Añadir el punto más cercano al mapa
            folium.Marker(
                [punto_mas_cercano.geometry.y, punto_mas_cercano.geometry.x],
                popup=f"{nombre}<br>Dirección: {direccion}<br>Puntuación: \
                        {puntuacion}<br># de calificaciones: {calificaciones}",
                icon=folium.Icon(color='green')
            ).add_to(m)

            # Añadir línea entre el punto dado y el punto más cercano
            folium.PolyLine(locations=[(coords['latitude'],
                                        coords['longitude']),
                                       (punto_mas_cercano.geometry.y,
                                        punto_mas_cercano.geometry.x)],
                            color='blue').add_to(m)

            # Añadir el resto de los puntos al mapa
            for _, row in gdf.iterrows():
                if row.name != punto_mas_cercano.name:
                    folium.Marker(
                        [row.geometry.y, row.geometry.x],
                        popup=f"{row['name']}<br>Dirección: \
                                {row['vicinity']}<br>Puntuación: \
                                {row['rating']}<br># de calificaciones: \
                                {row['user_ratings_total']}",
                        icon=folium.Icon(color='blue')
                    ).add_to(m)
            return m, punto_mas_cercano

        # Crear el mapa
        m, punto_mas_cercano = crear_mapa(coords, gdf)

        # Mostrar el punto más cercano
        st.write("Punto más cercano:")

        # Información del punto más cercano
        nombre = punto_mas_cercano['name']
        direccion = punto_mas_cercano['vicinity']
        puntuacion = punto_mas_cercano['rating']
        calificaciones = punto_mas_cercano['user_ratings_total']
        punto_mas_cercano = f"{nombre}\nDirección: {direccion}\nPuntuación: \
                              {puntuacion}\n# de calificaciones: \
                              {calificaciones}"

        st.write(punto_mas_cercano)

        # Mostrar el mapa
        st_folium.folium_static(m, width=700, height=500)
