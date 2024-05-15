"""
Este módulo implementa la validación de los campos de registro de un nuevo
usuario, incluyendo el nombre, correo electrónico, nombre de usuario y
contraseña.
"""

# Importar las librerías necesarias
# - re: Módulo que implementa expresiones regulares en Python.
# - streamlit: Framework utilizado para construir aplicaciones web en Python.
import re


class Validator:
    """
    Esta clase se encarga de validar la entrada de usuario para nombres de
    usuario, nombres, correos electrónicos y contraseñas. Proporciona métodos
    para asegurar que las entradas de usuario cumplan con los criterios
    especificados para seguridad y formato.
    """
    def __init__(self):
        """
        Inicializa la clase Validator con patrones de expresiones regulares
        para validar correos electrónicos, nombres y nombres de usuario, así
        como los requisitos de seguridad para las contraseñas.
        """

        self.email_pattern = re.compile(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
        self.name_pattern = re.compile(r"^[A-Za-z ]+$")
        self.username_pattern = re.compile(r"^[a-zA-Z0-9_-]{1,20}$")
        self.password_requirements = {
            "min_length": 8,
            "upper": re.compile(r"[A-Z]"),
            "lower": re.compile(r"[a-z]"),
            "digit": re.compile(r"[0-9]"),
            "special": re.compile(r"[!@#$%^&*(),.?\":{}|<>]")
        }

    def validate_email(self, email: str) -> bool:
        """
        Valida el formato y la longitud del correo electrónico.

        Args:
            email (str): El correo electrónico a validar.

        Returns:
            bool: Verdadero si el correo es válido, Falso en caso contrario.
        """
        return bool(self.email_pattern.match(email)) and 2 < len(email) < 320

    def validate_name(self, name: str) -> bool:
        """
        Valida el formato y la longitud del nombre.

        Args:
            name (str): El nombre a validar.

        Returns:
            bool: Verdadero si el nombre es válido, Falso en caso contrario.
        """
        return bool(self.name_pattern.match(name)) and 1 <= len(name) <= 100

    def validate_username(self, username: str) -> bool:
        """
        Valida el formato del nombre de usuario y verifica
        la ausencia de espacios.

        Args:
            username (str): El nombre de usuario a validar.

        Returns:
            bool: Verdadero si el nombre de usuario es válido,
                    Falso en caso contrario.
        """
        return bool(self.username_pattern.match(username))

    def validate_password_strength(self, password: str) -> str:
        """
        Verifica si la contraseña cumple con los requisitos de seguridad.

        Args:
            password (str): La contraseña a validar.

        Returns:
            str: 'ok' si la contraseña es fuerte, de lo contrario devuelve
                    un mensaje de error.
        """

        result = ""

        if " " in password:
            result = "La contraseña no puede contener espacios."
        elif len(password) < self.password_requirements["min_length"]:
            result = "La contraseña debe tener al menos 8 caracteres."
        elif not self.password_requirements["lower"].search(password):
            result = "La contraseña debe contener al menos una letra \
                            minúscula."
        elif not self.password_requirements["upper"].search(password):
            result = "La contraseña debe contener al menos una letra \
                            mayúscula."
        elif not self.password_requirements["digit"].search(password):
            result = "La contraseña debe contener al menos un dígito \
                            numérico."
        elif not self.password_requirements["special"].search(password):
            result = "La contraseña debe contener al menos un símbolo \
                            especial (ej. !@#$%^&*(),.?\":{}|<>)."
        else:
            result = "ok"

        return result

    def validate_registration_fields(self, name, email, username,
                                     password, confirm_password):
        """
        Valida todos los campos de registro para un nuevo usuario.

        Args:
            name (str): Nombre del usuario.
            email (str): Correo electrónico del usuario.
            username (str): Nombre de usuario del usuario.
            password (str): Contraseña del usuario.
            confirm_password (str): Confirmación de la contraseña del usuario.

        Returns:
            bool: Verdadero si todos los campos son válidos, Falso
                    en caso contrario.
        """

        result = False

        # Validar los campos de registro
        password_strength = self.validate_password_strength(password)

        if not (name and self.validate_name(name)):
            message = "Por favor, introduce un nombre válido sin caracteres."
            result = False, message
        elif not (email and self.validate_email(email)):
            message = "Por favor, introduce un correo electrónico válido."
            result = False, message
        elif not (username and self.validate_username(username)):
            message = "Por favor, introduce un nombre de usuario válido."
            result = False, message
        elif not password:
            message = "Por favor, introduce una contraseña."
            result = False, message
        elif password != confirm_password:
            message = "Las contraseñas no coinciden."
            result = False, message
        elif password_strength != "ok":
            message = password_strength
            result = False, message

        else:
            result = True, "ok"

        return result

    def validate_length(self, variable: str, min_length: int = 0,
                        max_length: int = 100) -> bool:
        """
        Checks the length of a variable.

        Parameters
        ----------
        variable: str
            The variable to be validated.
        min_length: str
            The minimum required length for the variable.
        max_length: str
            The maximum required length for the variable.

        Returns
        -------
        bool
            Validity of entered variable.
        """
        return min_length <= len(variable) <= max_length
