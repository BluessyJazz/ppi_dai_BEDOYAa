"""
Wily MotoTrack - Aplicación para el registro de
gastos e ingresos de motociclistas.

Este módulo contiene la implementación de la aplicación principal
utilizando Streamlit.
"""

# Importar streamlit
import streamlit as st
from modules.menus import Menu

# Configurar la página
st.set_page_config(
    page_title="Wily MotoTrack",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Si no se ha iniciado sesión, mostrar la página de inicio de sesión
menu = Menu()
menu.land_page()
