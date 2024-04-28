"""
Este módulo contiene la clase para la conexión a la base de datos PostgreSQL. 
"""

# Importar las librerías
# Streamlit para acceder a las variables de entorno
import streamlit as st
# La biblioteca psycopg2 para la conexión con PostgreSQL
import psycopg2


# Definir la clase para la conexión a la base de datos
class ConexionDB: 
    """Clase para la conexión a la base de datos PostgreSQL."""

    def __init__(self):
        """Inicializa la conexión a la base de datos."""
        self.conn = None


    def conectar(self):
        """
        Establece una conexión con la base de datos PostgreSQL.

        Returns:
            psycopg2.extensions.connection: Un objeto
            de conexión a la base de datos.
        """
        # Establece una conexión con la base de datos PostgreSQL
        self.conn = psycopg2.connect(
            dbname=st.secrets['postgresqlconn']['database'],
            user=st.secrets['postgresqlconn']['username'],
            password=st.secrets['postgresqlconn']['password'],
            host=st.secrets['postgresqlconn']['host'],
            port=st.secrets['postgresqlconn']['port']
        )
        return self.conn


    def cerrar(self):
        """Cerrar la conexión a la base de datos."""
        if self.conn is not None:
            self.conn.close()
            self.conn = None
