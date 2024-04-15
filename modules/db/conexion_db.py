"""
Este módulo contiene la implementación de
la conexión a la base de datos PostgreSQL.
"""

# Importa la biblioteca psycopg2 para la conexión con PostgreSQL
import psycopg2


def conectar_db():
    """
    Establece una conexión con la base de datos PostgreSQL.

    Returns:
        psycopg2.extensions.connection: Un objeto
        de conexión a la base de datos.
    """
    # Establece una conexión con la base de datos PostgreSQL
    conn = psycopg2.connect(
        dbname='wilymoto',  # Nombre de la base de datos
        user='bluessyjazz',  # Nombre de usuario
        password='Vg74PiTzYAfyVtacoFO7lhUJJiqtekAU',  # Contraseña
        host='dpg-coekj220si5c739jqg4g-a.oregon-'
             'postgres.render.com',  # Dirección del host
        port='5432'  # Puerto PostgreSQL por defecto
    )
    return conn
