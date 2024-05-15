"""
Este módulo levanta errores de Credenciales,
Deprecación, Olvido, Inicio de Sesión, Registro, Reinicio y Actualización.
"""


class CredentialsError(Exception):
    """
    Excepción levantada por credenciales incorrectas.

    Args:
        credential_type (str): Tipo de credencial incorrecta
            ('username', 'password', o ambos).

    Returns:
        None
    """

    def __init__(self, credential_type: str = ''):
        if credential_type == 'username':
            super().__init__('El nombre de usuario es incorrecto')
        elif credential_type == 'password':
            super().__init__('La contraseña es incorrecta')
        else:
            super().__init__('Nombre de usuario/contraseña incorrectos')


class DeprecationError(Exception):
    """
    Excepción levantada por funcionalidades depreciadas.

    Args:
        message (str): Mensaje de error personalizado para mostrar.

    Returns:
        None
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ForgotError(Exception):
    """
    Excepción levantada para los widgets de nombre de usuario o
    contraseña olvidados.

    Args:
        message (str): Mensaje de error personalizado para mostrar.

    Returns:
        None
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class LoginError(Exception):
    """
    Excepción levantada para el widget de inicio de sesión.

    Args:
        message (str): Mensaje de error personalizado para mostrar.

    Returns:
        None
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class RegisterError(Exception):
    """
    Excepción levantada para el widget de registro de usuario.

    Args:
        message (str): Mensaje de error personalizado para mostrar.

    Returns:
        None
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ResetError(Exception):
    """
    Excepción levantada para el widget de restablecimiento de contraseña.

    Args:
        message (str): Mensaje de error personalizado para mostrar.

    Returns:
        None
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UpdateError(Exception):
    """
    Excepción levantada para el widget de actualización de detalles de usuario.

    Args:
        message (str): Mensaje de error personalizado para mostrar.

    Returns:
        None
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
