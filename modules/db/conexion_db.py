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

    def obtener_registro_financiero(self, user_id):
        """
        Obtiene los registros financieros de un usuario de la base de datos.

        Args:
            user_id (int): El ID del usuario.

        Returns:
            list: Una lista de tuplas con los registros financieros.
        """
        # Conectar a la base de datos
        conn = self.conectar()

        # Crear un cursor
        cursor = conn.cursor()

        # Consultar los registros financieros del usuario
        cursor.execute(
            "SELECT id, actividad, tipo, monto, descripcion, fecha "
            "FROM registros_financieros "
            "WHERE user_id = %s", (user_id,))

        # Obtener todos los registros
        registros = cursor.fetchall()

        # Cerrar la conexión
        self.cerrar()

        return registros

    def modificar_registro_financiero(self, user_id, actividad, tipo, monto, descripcion, fecha_hora, registro):
        """
        Modifica un registro financiero existente.

        Args:
            user_id (int): El ID del usuario.
            actividad (str): La actividad del registro.
            tipo (str): El tipo de registro (Gasto, Ingreso, etc.).
            monto (float): El monto del registro.
            descripcion (str): La descripción del registro.
            fecha_hora (datetime): La fecha y hora del registro.
            registro (int): El ID del registro a modificar.

        Returns:
            None
        """
        # Conectar a la base de datos
        self.conectar()

        # Crear un cursor
        cursor = self.conn.cursor()

        # Actualizar el registro
        cursor.execute("""
            UPDATE registros_financieros
            SET actividad = %s, tipo = %s, monto = %s, descripcion = %s, fecha = %s
            WHERE id = %s AND user_id = %s
        """, (actividad, tipo, monto, descripcion, fecha_hora, registro, user_id))

        # Confirmar los cambios
        self.conn.commit()

        # Cerrar la conexión
        self.cerrar()

    def eliminar_registro_financiero(self, user_id, registro):
        """
        Elimina un registro financiero existente.

        Args:
            user_id (int): El ID del usuario.
            registro (int): El ID del registro a eliminar.

        Returns:
            None
        """
        # Crear una conexión a la base de datos
        conn = self.conectar()

        # Crear la consulta SQL para eliminar el registro
        query = """
        DELETE FROM registros_financieros
        WHERE user_id = %s AND id = %s
        """
        params = (user_id, registro)

        # Ejecutar la consulta SQL
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

        # Cerrar la conexión a la base de datos
        self.cerrar()

    def actualizar_contrasena(self, username, password):
        """
        Actualiza la contraseña de un usuario en la base de datos.

        Args:
            username (str): El nombre de usuario del usuario.
            password (str): La nueva contraseña del usuario.

        Returns:
            None
        """

        # Conectar a la base de datos
        conn = self.conectar()

        # Crear un cursor
        cursor = conn.cursor()

        # Actualizar la contraseña del usuario en la base de datos
        cursor.execute(
            "UPDATE usuarios SET contrasena = %s WHERE usuario = %s",
            (password, username)
        )

        # Guardar los cambios
        conn.commit()

        # Cerrar el cursor
        self.cerrar()

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
