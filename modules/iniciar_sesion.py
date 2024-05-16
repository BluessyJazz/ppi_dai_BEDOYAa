"""
Página de inicio de sesión
"""

# Importar librerías
import yaml
import streamlit as st
import streamlit.components.v1 as components
from yaml.loader import SafeLoader

from menu import menu
from modules.auth import init_auth
from modules.db.conexion_db import ConexionDB
from modules.auth.authenticate import Authenticate
from modules.utilities.exceptions import (LoginError)

'''
# Configuración de la página
st.set_page_config(
    page_title="Iniciar sesión · Wily MotoTrack",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="expanded",
)


auth = init_auth()
'''


def login(auth):
    try:
        auth.login()
    except LoginError as e:
        st.error(e)

    if st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

    st.markdown("""
                Si no tienes una cuenta, puedes
                [registrarte](/registrarse).
                """)


st.session_state
