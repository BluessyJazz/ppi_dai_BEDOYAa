import sqlite3


def crear_tablas():
    """
    Crea la estructura de la base de datos.
    """
    conexion = sqlite3.connect('usuarios.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            correo_electronico TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    crear_tablas()
