"""
Este módulo contiene la lógica para la autenticación de usuarios.
"""

# Importar librerías
# -streamlit: para crear aplicaciones web
import streamlit as st

# Importar módulos
# -db: para interactuar con la base de datos
# -authenticate: para autenticar a los usuarios
from modules.db import ConexionDB
from .authenticate import Authenticate


def init_auth():
    """
    Inicializa la autenticación de usuarios.

    Args:
        None

    Returns:
        Authenticate: Una instancia de la clase Authenticate para la
        autenticación de usuarios.
    """
    # Cargar las credenciales de la base de datos
    conexion_db = ConexionDB()

    # Obtener los usuarios y sus credenciales
    usuarios = conexion_db.obtener_usuarios()

    # Crear una instancia de la clase Authenticate
    auth = Authenticate(
        usuarios,
        st.secrets['cookie']['name'],
        st.secrets['cookie']['key'],
        st.secrets['cookie']['expiry_days']
    )

    return auth
