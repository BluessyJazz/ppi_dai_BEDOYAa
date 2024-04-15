"""
Este módulo contiene la función para crear
un nuevo usuario en la base de datos.
"""

# Importar librerías
from psycopg2 import sql  # Para evitar SQL Injection
from .conexion_db import conectar_db  # Para conectar a la base de datos
from .verificar_usuario import verificar_usuario  # Para verificar si el
# usuario ya existe


def crear_usuario(nombre, correo, contrasena):
    """Crea un nuevo usuario en la base de datos.

    Args:
        nombre (str): El nombre del usuario.
        correo (str): El correo electrónico del usuario.
        contrasena (str): La contraseña del usuario.

    Returns:
        None
    """
    # Verificar si el usuario ya existe en la base de datos
    if not verificar_usuario(nombre, correo):
        # Conectar a la base de datos
        conn = conectar_db()
        cursor = conn.cursor()

        # Consulta SQL para insertar el nuevo usuario
        query = sql.SQL("INSERT INTO usuarios (nombre, correo, "
                        "contrasena, rol) VALUES (%s, %s, %s, %s)")
        cursor.execute(query, (nombre, correo, contrasena, 'usuario'))

        # Guardar los cambios en la base de datos
        conn.commit()
        conn.close()
