
from psycopg2 import sql
from .conexion_db import conectar_db
from .verificar_usuario import verificar_usuario


def crear_usuario(nombre, correo, contrasena):
    """Crea un nuevo usuario en la base de datos."""
    if not verificar_usuario(nombre, correo):
        conn = conectar_db()
        cursor = conn.cursor()

        # Consulta SQL para insertar el nuevo usuario
        query = sql.SQL("INSERT INTO usuarios (nombre, correo, contrasena, rol) "
                        "VALUES (%s, %s, %s, %s)")
        cursor.execute(query, (nombre, correo, contrasena, 'usuario'))

        conn.commit()
        conn.close()