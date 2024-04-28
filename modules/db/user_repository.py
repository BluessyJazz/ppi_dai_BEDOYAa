"""
Este módulo contiene la implementación de la clase UserRepository
para interactuar con la base de datos de usuarios.
"""

# Importar librerías necesarias para la conexión a la base de datos
from contextlib import contextmanager
from .conexion_db import ConexionDB


class UserRepository:
    """
    Repositorio para manejar las operaciones de la base de
    datos para usuarios en PostgreSQL.
    """

    def __init__(self):
        """
        Inicializa UserRepository con una nueva instancia de ConexionDB.

        Args:
            db_connection (ConexionDB): Una instancia de ConexionDB.
        """

        self.db_connection = ConexionDB()

    @contextmanager
    def manage_db_connection(self):
        """
        Gestiona la conexión a la base de datos asegurando
        que se cierre apropiadamente.

        Yields:
            psycopg2.extensions.connection: Un objeto
            de conexión a la base de datos.

        Raises:
            Exception: Si ocurre un error al conectar a la base de datos.
        """

        # Inicializar las variables de conexión y cursor
        cursor = None
        conn = None

        try:
            conn = self.db_connection.conectar()
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                self.db_connection.cerrar()

    def fetch_users(self):
        """
        Consulta y recupera todos los usuarios de la base de datos.

        Returns:
            list: Una lista de diccionarios con los 
            usuarios de la base de datos.
        """

        with self.manage_db_connection() as cursor:
            cursor.execute("SELECT * FROM usuarios")
            users = cursor.fetchall()
            return users

    def create_user(self, nombre, correo, contrasena, rol):
        """
        Crea un nuevo usuario en la base de datos.

        Args:
            nombre (str): El nombre del usuario.
            correo (str): El correo electrónico del usuario.
            contrasena (str): La contraseña del usuario.
            rol (str): El rol del usuario.

        Returns:
            int: El número de filas afectadas por la operación.
        """

        with self.manage_db_connection() as cursor:
            cursor.execute(
                "INSERT INTO usuarios (nombre, correo, contrasena, rol) \
                    VALUES (%s, %s, %s, %s)",
                (nombre, correo, contrasena, rol)
            )
            return cursor.rowcount

    def fetch_user_by_name(self, nombre):
        """
        Consulta y recupera un usuario por su nombre.

        Args:
            nombre (str): El nombre del usuario a buscar.

        Returns:
            dict: Un diccionario con la información del usuario.
        """

        with self.manage_db_connection() as cursor:
            cursor.execute("SELECT * FROM usuarios \
                WHERE nombre = %s", (nombre,))
            user = cursor.fetchone()
            return user

    def fetch_user_by_email(self, correo):
        """
        Consulta y recupera un usuario por su correo electrónico.

        Args:
            correo (str): El correo electrónico del usuario a buscar.

        Returns:
            dict: Un diccionario con la información del usuario.
        """

        with self.manage_db_connection() as cursor:
            cursor.execute("SELECT * FROM usuarios \
                WHERE correo = %s", (correo,))
            user = cursor.fetchone()
            return user

    def update_user(self, nombre, correo, contrasena, rol):
        """
        Actualiza un usuario en la base de datos.

        Args:
            nombre (str): El nombre del usuario.
            correo (str): El correo electrónico del usuario.
            contrasena (str): La contraseña del usuario.
            rol (str): El rol del usuario.

        Returns:
            int: El número de filas afectadas por la operación.
        """

        with self.manage_db_connection() as cursor:
            cursor.execute(
                "UPDATE usuarios SET correo = %s, contrasena = %s, rol = %s \
                    WHERE nombre = %s",
                (correo, contrasena, rol, nombre)
            )
            return cursor.rowcount

    def update_user_password(self, correo, contrasena):
        """
        Actualiza la contraseña de un usuario en la base de datos.

        Args:
            correo (str): El correo electrónico del usuario.
            contrasena (str): La nueva contraseña del usuario.

        Returns:
            int: El número de filas afectadas por la operación.
        """

        with self.manage_db_connection() as cursor:
            cursor.execute(
                "UPDATE usuarios SET contrasena = %s WHERE correo = %s",
                (contrasena, correo)
            )
            return cursor.rowcount

    def delete_user(self, correo):
        """
        Elimina un usuario de la base de datos.

        Args:
            correo (str): El correo electrónico del usuario a eliminar.

        Returns:
            int: El número de filas afectadas por la operación.
        """

        with self.manage_db_connection() as cursor:
            cursor.execute("DELETE FROM usuarios WHERE correo = %s", (correo,))
            return cursor.rowcount

    def verify_user(self, nombre, correo):
        """
        Verifica si un usuario ya existe en la base de datos.

        Args:
            nombre (str): El nombre del usuario a verificar.
            correo (str): El correo del usuario a verificar.

        Returns:
            bool: True si el usuario existe, False en caso contrario.
        """

        with self.manage_db_connection() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE nombre = %s \
                OR correo = %s", (nombre, correo))
            user = cursor.fetchone()
            return user is not None

    def verify_credentials(self, username, password):
        """
        Verifica las credenciales del usuario para el inicio de sesión.

        Args:
            username (str): El nombre de usuario.
            password (str): La contraseña del usuario.

        Returns:
            bool: True si las credenciales son correctas,
            False en caso contrario.
        """
        with self.manage_db_connection() as cursor:
            cursor.execute(
                "SELECT * FROM usuarios WHERE nombre = %s AND contrasena = %s",
                (username, password)
            )
            return cursor.fetchone() is not None
