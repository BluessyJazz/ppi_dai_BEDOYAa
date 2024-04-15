import psycopg2
from psycopg2 import sql
from .conexion_db import conectar_db


def verificar_usuario(nombre, correo):
    """Verifica si un usuario ya existe en la base de datos."""
    conn = conectar_db()
    cursor = conn.cursor()

    # Consulta SQL para verificar si el usuario ya existe
    query = sql.SQL("SELECT * FROM usuarios WHERE nombre = %s OR correo = %s")
    cursor.execute(query, (nombre, correo))

    usuario = cursor.fetchone()
    conn.close()

    # Si el usuario existe, devolver True, de lo contrario, devolver False
    return usuario is not None