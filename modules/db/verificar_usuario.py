"""
Este módulo contiene la función para verificar
si un usuario ya existe en la base de datos.
"""

# Importar librerías necesarias para conectarse a la base de datos
from psycopg2 import sql  # Para evitar SQL Injection
from .conexion_db import conectar_db  # Para conectar a la base de datos


def verificar_usuario(nombre, correo):
    """Verifica si un usuario ya existe en la base de datos.

    Args:
        nombre (str): El nombre del usuario a verificar.
        correo (str): El correo del usuario a verificar.

    Returns:
        bool: True si el usuario existe, False en caso contrario.
    """
    # Conectar a la base de datos
    conn = conectar_db()

    # Crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # Consulta SQL para verificar si el usuario ya existe
    query = sql.SQL("SELECT * FROM usuarios WHERE nombre = %s OR correo = %s")
    
    # Ejecutar la consulta con los parámetros correspondientes
    cursor.execute(query, (nombre, correo))

    # Obtener el primer resultado de la consulta
    usuario = cursor.fetchone()

    # Cerrar la conexión a la base de datos
    conn.close()

    # Si el usuario existe, devolver True, de lo contrario, devolver False
    return usuario is not None
