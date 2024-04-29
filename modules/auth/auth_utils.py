"""
Este módulo contiene la clase para
la autenticación de usuarios.
"""

# Importar las librerías necesarias
import yaml
import streamlit_authenticator as stauth
from modules.db.user_repository import UserRepository


class AuthUtils:
    """
    Clase para las utilidades de autenticación.
    """

    def __init__(self):
        """Inicializa la clase AuthUtils."""
        self.user_repo = UserRepository()

    def generate_temp_config(self):
        """
        Genera un archivo de configuración temporal
        para la autenticación de usuarios.

        Returns:
            dict: Un diccionario con la configuración
            de autenticación.
        """

        # Obtener los usuarios de la base de datos
        users = self.user_repo.fetch_users()

        # Crear el archivo de configuración temporal
        config = {
            'credentials': {
                'usernames': {
                    user[3]: {
                        'email': user[2],
                        'failed_attempts': 0,
                        'logged_in': False,
                        'name': user[1],
                        'password': user[4]
                    }
                    for user in users
                }
            },
            'cookie': {
                'expiry_days': 30,
                'key': 'some_signature_key',
                'name': 'auth_cookie'
            }
        }

        with open('temp_config.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(config, file)

    def authenticate(self):
        """
        Autentica a un usuario y devuelve su nombre y estado de autenticación.

        Returns:
            tuple: Una tupla con el nombre del usuario,
            el estado de autenticación y el nombre de usuario.
        """

        # Generar el archivo de configuración temporal
        self.generate_temp_config()

        # Cargar la configuración de autenticación
        with open('temp_config.yaml', 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)

        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days']
        )

        return authenticator
