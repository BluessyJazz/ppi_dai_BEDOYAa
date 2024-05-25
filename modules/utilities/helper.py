"""
Este módulo ejecuta la lógica para generar una clave aleatoria.
"""

# Importar las librerías necesarias
# - string: Módulo que implementa constantes de cadenas de texto.
# - random: Módulo que implementa generación de números aleatorios.
import string
import random


class Helper:
    """
    Esta clase ejecuta la lógica para funciones varias.
    """

    def __init__(self):
        pass

    @classmethod
    def generate_random_pw(cls, length: int = 16) -> str:
        """
        Genera una contraseña aleatoria.

        Args:
            length (int): La longitud de la contraseña generada.

        Returns:
            str: La contraseña generada aleatoriamente.
        """
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(length)).replace(' ', '')
