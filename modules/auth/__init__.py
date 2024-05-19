"""
Este módulo contiene la lógica para la autenticación de usuarios.
"""

import yaml
from yaml.loader import SafeLoader
from modules.db import ConexionDB
from .authenticate import Authenticate


def init_auth():
    """
    Inicializa la autenticación de usuarios.
    """

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

    return auth
