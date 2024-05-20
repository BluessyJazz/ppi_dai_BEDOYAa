"""
Página de inicio de sesión
"""

# Importar librerías
import streamlit as st
import streamlit.components.v1 as components

from menu import menu
from modules.db.conexion_db import ConexionDB
from modules.auth import init_auth
from modules.utilities.exceptions import (LoginError)


# Configuración de la página
st.set_page_config(
    page_title="Iniciar sesión · Wily MotoTrack",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Inicializar la autenticación
auth = init_auth()

# Establecer conexión con la base de datos
conexion_db = ConexionDB()

auth.login()


if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
    menu(auth=None)
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
    menu(auth=None)
elif st.session_state["authentication_status"] is True:
    st.success('You are now logged in!')
    conexion_db.actualizar_estado_login(st.session_state["username"], True)
    menu(auth=auth)
    st.switch_page("main.py")

st.markdown("""
            Si no tienes una cuenta, puedes
            [registrarte](/registro).
            """)
