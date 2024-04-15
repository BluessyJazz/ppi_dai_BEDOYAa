import psycopg2
from psycopg2 import sql

def conectar_db():
    """Establece una conexión a la base de datos PostgreSQL."""

    conn = psycopg2.connect(
        dbname='wilymoto',
        user='bluessyjazz',
        password='Vg74PiTzYAfyVtacoFO7lhUJJiqtekAU',
        host='dpg-coekj220si5c739jqg4g-a.oregon-postgres.render.com',
        port='5432'  # Puerto predeterminado de PostgreSQL
    )
    return conn