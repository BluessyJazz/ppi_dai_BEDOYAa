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
    """
    Clase para la conexión a la base de datos PostgreSQL.
    """

    def __init__(self):
        """Inicializa la conexión a la base de datos."""

        # Inicializa la conexión como nula
        self.conn = None

    def conectar(self):
        """
        Establece una conexión con la base de datos PostgreSQL.

        Args:
            None

        Returns:
            psycopg2.extensions.connection: Un objeto
            de conexión a la base de datos.
        """

        self.conn = psycopg2.connect(
            dbname=st.secrets['postgresqlconn']['database'],
            user=st.secrets['postgresqlconn']['username'],
            password=st.secrets['postgresqlconn']['password'],
            host=st.secrets['postgresqlconn']['host'],
            port=st.secrets['postgresqlconn']['port']
        )

        return self.conn

    def obtener_usuarios(self):
        """
        Obtiene los usuarios y sus credenciales de la base de datos y los
        devuelve en un diccionario.

        Args:
            None

        Returns:
            dict: Un diccionario que contiene los usuarios y sus credenciales.
        """
        # Conecta a la base de datos
        conn = self.conectar()

        # Crea un cursor
        cursor = conn.cursor()

        # Ejecuta la consulta SQL para obtener los usuarios y sus credenciales
        cursor.execute("SELECT usuario, correo, logged_in, nombre, contrasena,"
                       " id FROM usuarios")

        # Obtiene todos los registros
        registros = cursor.fetchall()

        # Cierra la conexión
        self.cerrar()

        # Crea un diccionario para almacenar los usuarios y sus credenciales
        usuarios = {'usernames': {}}

        # Itera sobre los registros y los añade al diccionario
        for registro in registros:
            usuarios['usernames'][registro[0]] = {
                'email': registro[1],
                'logged_in': registro[2],
                'name': registro[3],
                'password': registro[4],
                'id': registro[5]
            }

        return usuarios

    def actualizar_estado_login(self, username, logged_in):
        """
        Actualiza el estado de inicio de sesión de un usuario en la base
        de datos.

        Args:
            username (str): El nombre de usuario del usuario.
            logged_in (bool): El estado de inicio de sesión del usuario.

        Returns:
            None
        """

        # Conectar a la base de datos
        conn = self.conectar()

        # Crear un cursor
        cursor = conn.cursor()

        # Actualizar el estado de inicio de sesión del usuario en la
        # base de datos
        cursor.execute(
            "UPDATE usuarios SET logged_in = %s WHERE usuario = %s",
            (logged_in, username)
        )

        # Guardar los cambios
        conn.commit()

        # Cerrar el cursor
        self.cerrar()

    def insertar_usuario(self, email, username, name, password):
        """
        Inserta un nuevo usuario en la base de datos.

        Args:
            email (str): El correo electrónico del usuario.
            username (str): El nombre de usuario.
            name (str): El nombre del usuario.
            password (str): La contraseña del usuario.

        Returns:
            None
        """

        # Conectar a la base de datos
        conn = self.conectar()

        # Crear un cursor
        cursor = conn.cursor()

        # Insertar el nuevo usuario en la base de datos
        cursor.execute(
            "INSERT INTO usuarios (correo, usuario, nombre, contrasena)"
            "VALUES (%s, %s, %s, %s)", (email, username, name, password))

        # Guardar los cambios
        conn.commit()

        # Cerrar el cursor
        self.cerrar()

    def insertar_registro_financiero(self, actividad, tipo, monto,
                                     descripcion, fecha, user_id):
        """
        Inserta un nuevo registro financiero en la base de datos.

        Args:
            user_id (int): El ID del usuario.
            tipo (str): El tipo de transacción (gasto o ingreso).
            monto (float): El monto de la transacción.
            descripcion (str, optional): La descripción de la transacción.

        Returns:
            None
        """
        # Conectar a la base de datos
        conn = self.conectar()

        # Crear un cursor
        cursor = conn.cursor()

        import pytz
        from datetime import datetime

        def obtener_hora_colombiana():
            zona_horaria_colombia = pytz.timezone('America/Bogota')
            hora_actual_utc = datetime.now(pytz.utc)
            return hora_actual_utc.astimezone(zona_horaria_colombia)

        fecha = obtener_hora_colombiana()

        # Insertar el nuevo registro financiero en la base de datos
        cursor.execute(
            "INSERT INTO registros_financieros "
            "(actividad, tipo, monto, descripcion, fecha, user_id) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (actividad, tipo, monto, descripcion, fecha, user_id)
        )

        # Guardar los cambios
        conn.commit()

        # Cerrar el cursor y la conexión
        self.cerrar()

    def cerrar(self):
        """
        Cerrar la conexión a la base de datos.

        Args:
            None

        Returns:
            None
        """
        if self.conn is not None:
            self.conn.close()
            self.conn = None
