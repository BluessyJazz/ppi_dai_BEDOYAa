"""
Página de inicio de sesión
"""

# Importar librerías
import yaml
import streamlit as st
import streamlit.components.v1 as components
from yaml.loader import SafeLoader

from menu import menu
from modules.db.conexion_db import ConexionDB
from modules.auth.authenticate import Authenticate
from modules.utilities.exceptions import (LoginError)

# Configuración de la página
st.set_page_config(
    page_title="Iniciar sesión · Wily MotoTrack",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Cargar las credenciales de la base de datos
conexion_db = ConexionDB()

# Obtener los usuarios y sus credenciales
usuarios = conexion_db.obtener_usuarios()

# Cargar el archivo de configuración
with open("config.yaml", "r", encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Crear una instancia de la clase Authenticate
auth = Authenticate(
    usuarios,
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    auth.login()
except LoginError as e:
    st.error(e)

if st.session_state['authentication_status']:
    st.write(f'Bienvenido {st.session_state["username"]}')
    st.session_state['auth'] = auth
    st.switch_page("main.py")
if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
    menu(auth=None)
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
    menu(auth=None)

st.markdown("""
            Si no tienes una cuenta, puedes
            [registrarte](/registrarse).
            """)
