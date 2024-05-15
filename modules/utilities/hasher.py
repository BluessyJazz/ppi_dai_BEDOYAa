"""
Este módulo ejecuta la lógica para el hash de contraseñas en texto plano.
"""

# Importar las librerías necesarias
# - re: Módulo que implementa expresiones regulares.
# - bcrypt: Módulo que implementa hashing seguro para texto plano.
import re
import bcrypt


class Hasher:
    """
    Esta clase realiza el hash de contraseñas en texto plano.
    """
    def __init__(self, passwords: list):
        """
        Crea una nueva instancia de "Hasher".

        Args:
            passwords (list): Lista de contraseñas en texto plano para
                                ser hasheadas.
        """
        self.passwords = passwords

    @classmethod
    def check_pw(cls, password: str, hashed_password: str) -> bool:
        """
        Verifica la validez de una contraseña ingresada comparándola con
        su versión hasheada.

        Args:
            password (str): Contraseña en texto plano para verificar.
            hashed_password (str): Contraseña hasheada con la que se compara.

        Returns:
            bool: Verdad si la contraseña coincide con la hasheada,
                    Falso en caso contrario.
        """
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def generate(self) -> list:
        """
        Realiza el hash de una lista de contraseñas en texto plano.

        Returns:
            list: Lista de contraseñas hasheadas.
        """
        return [self._hash(password) for password in self.passwords]

    @classmethod
    def _hash(cls, password: str) -> str:
        """
        Realiza el hash de una contraseña en texto plano.

        Args:
            password (str): La contraseña en texto plano a hashear.

        Returns:
            str: La contraseña hasheada.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @classmethod
    def _is_hash(cls, hash_string: str) -> bool:
        """
        Determina si una cadena de texto es un hash.

        Args:
            hash_string (str): Cadena que se sospecha es un hash.

        Returns:
            bool: Verdad si la cadena es un hash, Falso en caso contrario.
        """
        bcrypt_regex = re.compile(r'^\$2[aby]\$\d+\$.{53}$')
        return bool(bcrypt_regex.match(hash_string))
