"""
Este módulo implementa cookies para la re-autenticación sin contraseña.
"""

# Importar las librerías necesarias
# - datetime: Módulo que implementa tipos de datos DateTime.
# - jwt: Módulo que implementa Tokens Web JSON para Python.
# - streamlit: Framework utilizado para construir aplicaciones web en Python.
# - extra_streamlit_components: Módulo que implementa cookies para Streamlit.
from datetime import datetime, timedelta
import jwt
from jwt import DecodeError, InvalidSignatureError
import streamlit as st
import extra_streamlit_components as stx


class CookieHandler:
    """
    Esta clase ejecutará todas las acciones relacionadas con la cookie de
    re-autenticación, incluida la recuperación, eliminación y configuración
    de la cookie.
    """
    def __init__(self, cookie_name: str, cookie_key: str,
                 cookie_expiry_days: float = 30.0):
        """
        Inicializa la clase CookieHandler con los parámetros especificados.

        Parameters:
            - cookie_name: str
                Nombre de la cookie almacenada en el navegador del cliente para
                la re-autenticación sin contraseña.

            - cookie_key: str
                Clave que se utilizará para cifrar la firma de la cookie de
                re-autenticación.

            - cookie_expiry_days: float
                Número de días antes de que la cookie de re-autenticación
                expire automáticamente en el navegador del cliente.
        """

        # Inicializar las variables de la clase
        self.cookie_name = cookie_name
        self.cookie_key = cookie_key
        self.cookie_expiry_days = cookie_expiry_days
        self.cookie_manager = stx.CookieManager()
        self.token = None
        self.exp_date = None

    def get_cookie(self) -> str:
        """
        Recupera la cookie de re-autenticación, si existe.

        Args:
            None

        Returns:
            str
                Cookie de re-autenticación.
        """

        # Recuperar la cookie de re-autenticación
        if st.session_state['logout']:
            return False

        # Verificar si la cookie de re-autenticación ya está almacenada
        self.token = self.cookie_manager.get(self.cookie_name)

        # Verificar si la cookie de re-autenticación es válida
        if self.token is not None:
            self.token = self._token_decode()

            # Devolver la cookie de re-autenticación
            if (self.token is not False and 'username' in self.token and
               self.token['exp_date'] > datetime.utcnow().timestamp()):

                return self.token

    def delete_cookie(self):
        """
        Elimina la cookie de re-autenticación.

        Args:
            None

        Returns:
            None
        """

        try:
            # Eliminar la cookie de re-autenticación
            self.cookie_manager.delete(self.cookie_name)

        except KeyError as e:
            # Manejar la excepción si la cookie no existe
            print(e)

    def set_cookie(self):
        """
        Configura la cookie de re-autenticación.

        Args:
            None

        Returns:
            None
        """

        # Configurar la cookie de re-autenticación
        self.exp_date = self._set_exp_date()

        # Codificar y almacenar la cookie de re-autenticación
        token = self._token_encode()

        # Almacenar la cookie de re-autenticación en el navegador del cliente
        self.cookie_manager.set(self.cookie_name, token,
                                expires_at=datetime.now() +
                                timedelta(days=self.cookie_expiry_days))

    def _set_exp_date(self) -> str:
        """
        Establece la fecha de caducidad de la cookie de re-autenticación.

        Args:
            None

        Returns:
            str
                Fecha de caducidad de la cookie de re-autenticación.
        """

        # Calcular la fecha de caducidad de la cookie de re-autenticación
        fecha = datetime.utcnow() + timedelta(days=self.cookie_expiry_days)

        return fecha.timestamp()

    def _token_decode(self) -> str:
        """
        Decodifica el contenido de la cookie de re-autenticación.

        Args:
            None

        Returns:
            str
                Contenido de la cookie de re-autenticación.
        """

        try:

            # Decodificar la cookie de re-autenticación
            decode = jwt.decode(self.token, self.cookie_key,
                                algorithms=['HS256'])

            return decode

        except InvalidSignatureError as e:

            # Manejar la excepción si la firma de la cookie no es válida
            print(e)

            # Eliminar la cookie de re-autenticación si la firma no es válida
            return False

        except DecodeError as e:

            # Manejar la excepción si la cookie no se puede decodificar
            print(e)

            # Eliminar la cookie de re-autenticación si no se puede decodificar
            return False

    def _token_encode(self) -> str:
        """
        Codifica el contenido de la cookie de re-autenticación.

        Args:
            None

        Returns:
            str
                Contenido de la cookie de re-autenticación codificado.
        """

        # Codificar el contenido de la cookie de re-autenticación
        encode = jwt.encode({'username': st.session_state['username'],
                             'exp_date': self.exp_date},
                            self.cookie_key,
                            algorithm='HS256')

        return encode
