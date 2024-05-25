"""
Este módulo contiene la implementación de la página de registro de usuarios
"""

# Importar librerías
import time
import yaml
import streamlit as st
import streamlit.components.v1 as components
from yaml.loader import SafeLoader

from menu import menu
from modules.db.conexion_db import ConexionDB
from modules.auth import init_auth
from modules.utilities.exceptions import (RegisterError)

# Configuración de la página
st.set_page_config(
    page_title="Registrarse · Wily MotoTrack",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Cargar las credenciales de la base de datos
conexion_db = ConexionDB()

# Obtener los usuarios y sus credenciales
usuarios = conexion_db.obtener_usuarios()

# Iniciar la autenticación
auth = init_auth()

try:
    (name_of_registered_user,
        email_of_registered_user,
        username_of_registered_user,
        password_of_registered_user) = auth.register_user()
except RegisterError as e:
    st.error(e)

st.markdown("""
        Si ya tienes una cuenta, puedes
        [iniciar sesión](/iniciar_sesion).
        """)

if email_of_registered_user:
    conexion_db.insertar_usuario(email_of_registered_user,
                                 username_of_registered_user,
                                 name_of_registered_user,
                                 password_of_registered_user)
    st.success("Ya tienes tu cuenta en la app! 👏🎉")
    st.write(f"[Inicia sesión](/iniciar_sesion) como \
             {username_of_registered_user} para comenzar a usar la app.")

    time.sleep(5)
    st.rerun()

menu(auth=None)
