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

# Inicializar el menú
menu = Menu()

# Si no se ha iniciado sesión, mostrar la página de inicio de sesión
if not st.session_state.get("authentication_status"):
    menu.land_page()

# Si se ha iniciado sesión, mostrar la página de usuario
else:
    menu.user_page()
