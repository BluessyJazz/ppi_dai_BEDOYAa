"""
Módulo de base de datos para la aplicación Wily MotoTrack.

Este módulo proporciona funciones para conectarse a la base de datos SQLite
y realizar operaciones como insertar usuarios.
"""

import sqlite3
import os


def conectar_db():
    """
    Establece la conexión con la base de datos.

    Returns:
        SQLiteConnection: Conexión a la base de datos.
    """
    ruta_basedatos = os.path.join(os.path.dirname(__file__),
                                  '../../data/usuarios.db')
    return sqlite3.connect(ruta_basedatos)


def insertar_usuario(nombre, correo, contrasena):
    """
    Inserta un nuevo usuario en la tabla de usuarios.

    Args:
        nombre (str): Nombre del usuario.
        correo (str): Correo electrónico del usuario.
        contrasena (str): Contraseña del usuario.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nombre, correo_electronico, contrasena)
        VALUES (?, ?, ?)
    ''', (nombre, correo, contrasena))
    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    pass  # Código para pruebas o ejecución de funciones
