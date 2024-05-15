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
    This class executes the logic for miscellaneous functions.
    """
    def __init__(self):
        pass

    @classmethod
    def generate_random_pw(cls, length: int = 16) -> str:
        """
        Generates a random password.

        Parameters
        ----------
        length: int
            The length of the returned password.
        Returns
        -------
        str
            The randomly generated password.
        """
        letters = string.ascii_letters + string.digits
        return ''.join(
                        random.choice(letters) for i in range(length)
                        ).replace(' ', '')
