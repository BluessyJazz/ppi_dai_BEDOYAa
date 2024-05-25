"""
Este módulo contiene la lógica para la autenticación de usuarios.
"""

# Importar librerías
# -time: para pausar la ejecución
# -typing: para anotaciones de tipos
# -streamlit: para crear aplicaciones web
import time
from typing import Optional
import streamlit as st

# Importar módulos
# -db: para interactuar con la base de datos
# -validator: para validar los campos de registro
# -cookie: para manejar las cookies
# -authentication: para manejar la autenticación
from ..db import ConexionDB
from ..utilities.validator import Validator
from .cookie import CookieHandler
from .authentication import AuthenticationHandler


class Authenticate:
    """
    Esta clase manejará todas las acciones relacionadas con la autenticación
    de usuarios, incluida la creación de cookies para la re-autenticación sin
    contraseña.
    """
    def __init__(self, credentials: dict, cookie_name: str, cookie_key: str,
                 cookie_expiry_days: float = 30.0,
                 validator: Optional[Validator] = None):
        """
        Inicializa la clase Authenticate.

        Args:
            - credentials: dict
                Diccionario que contiene los usuarios y sus credenciales.

            - cookie_name: str
                Nombre de la cookie almacenada en el navegador del cliente para
                la re-autenticación sin contraseña.

            - cookie_key: str
                Clave que se utilizará para cifrar la firma de la cookie de
                re-autenticación.

            - cookie_expiry_days: float
                Número de días antes de que la cookie de re-autenticación
                expire automáticamente en el navegador del cliente.

            - validator: Validator
                Instancia de la clase Validator para validar los campos de
                registro.

        Returns:
            None
        """
        self.authentication_handler = AuthenticationHandler(credentials,
                                                            validator)
        self.cookie_handler = CookieHandler(cookie_name,
                                            cookie_key,
                                            cookie_expiry_days)

        # Inicializar una instancia de la clase ConexionDB
        self.db = ConexionDB()

        if validator is not None:
            self.validator = validator
        else:
            self.validator = Validator()

    def get_username(self) -> str:
        """
        Devuelve el nombre de usuario del usuario autenticado.

        Args:
            None

        Returns:
            str: Nombre de usuario del usuario autenticado.
        """
        return st.session_state['username']

    def forgot_password(self, location: str = 'main', fields: dict = None,
                        clear_on_submit: bool = False) -> tuple:
        """
        Crea un widget para recuperar la contraseña.

        Args:
            location (str): Ubicación del widget de recuperación de contraseña,
                            'main' o 'sidebar'.
            fields (dict): Nombres renderizados de los campos/botones.
            clear_on_submit (bool): Configuración de limpiar al enviar,
                                    True: limpia los campos al enviar,
                                    False: mantiene los campos al enviar.

        Returns:
            tuple: Nombre de usuario asociado a la contraseña olvidada,
                   Correo asociado a la contraseña olvidada,
                   Nueva contraseña en texto plano que debe ser transferida
                   al usuario de forma segura.
        """
        if fields is None:
            fields = {'Form name': 'Contraseña olvidada',
                      'Username': 'Usuario',
                      'Submit': 'Enviar'}

        if location == 'main':
            forgot_password_form = st.form('Contraseña olvidada',
                                           clear_on_submit=clear_on_submit)
        elif location == 'sidebar':
            forgot_password_form = st.sidebar.form('Contraseña olvidada')

        # Para el subencabezado del formulario
        if 'Form name' not in fields:
            forgot_password_form.subheader('Contraseña olvidada')
        else:
            forgot_password_form.subheader(fields['Form name'])

        # Para el campo de entrada de texto del formulario
        if 'Username' not in fields:
            username = forgot_password_form.text_input('Usuario').lower()
        else:
            username = forgot_password_form.text_input(
                                                       fields['Username']
                                                       ).lower()

        # Para el botón de envío del formulario
        if 'Submit' not in fields:
            submit_button_clicked = (
                forgot_password_form.form_submit_button('Submit')
            )
        else:
            submit_button_clicked = (
                forgot_password_form.form_submit_button(fields['Submit'])
            )

        # Si el botón de envío del formulario se presiona,
        # llama al método forgot_password
        if submit_button_clicked:
            return self.authentication_handler.forgot_password(username)

        return None, None, None

    def forgot_username(self, location: str = 'main', fields: dict = None,
                        clear_on_submit: bool = False) -> tuple:
        """
        Crea un widget para recuperar el nombre de usuario.

        Args:
            location (str): Ubicación del widget de recuperación de nombre de
                            usuario, 'main' o 'sidebar'.
            fields (dict): Nombres renderizados de los campos/botones.
            clear_on_submit (bool): Configuración de limpiar al enviar,
                                    True: limpia los campos al enviar,
                                    False: mantiene los campos al enviar.

        Returns:
            tuple: Nombre de usuario olvidado que debe ser transferido al
                   usuario de forma segura,
                   Correo asociado al nombre de usuario olvidado.
        """
        if fields is None:
            fields = {'Form name': 'Olvidé mi usuario',
                      'Email': 'Correo', 'Submit': 'Enviar'}

        if location == 'main':
            forgot_username_form = st.form('Olvidé mi usuario',
                                           clear_on_submit=clear_on_submit)
        elif location == 'sidebar':
            forgot_username_form = st.sidebar.form('Olvidé mi usuario')

        # Para el subencabezado del formulario
        if 'Form name' not in fields:
            forgot_username_form.subheader('Olvidé mi usuario')
        else:
            forgot_username_form.subheader(fields['Form name'])

        # Para el campo de entrada de texto del formulario
        if 'Email' not in fields:
            email = forgot_username_form.text_input('Correo')
        else:
            email = forgot_username_form.text_input(fields['Email'])

        # Para el botón de envío del formulario
        if 'Submit' not in fields:
            submit_button_clicked = (
                forgot_username_form.form_submit_button('Enviar')
                )
        else:
            submit_button_clicked = (
                forgot_username_form.form_submit_button(fields['Submit'])
            )

        # Si el botón de envío del formulario se presiona,
        # llama al método forgot_username
        if submit_button_clicked:
            return self.authentication_handler.forgot_username(email)

        return None, email

    def login_with_cookie(self):
        """
        Intenta iniciar sesión con una cookie.

        Args:
            None

        Returns:
            bool: True si el inicio de sesión fue exitoso, False en caso
                  contrario.
        """
        token = self.cookie_handler.get_cookie()
        if token:
            self.authentication_handler.execute_login(token=token)
            time.sleep(0.7)

        name = st.session_state['name']
        authentication_status = st.session_state['authentication_status']
        username = st.session_state['username']

        return name, authentication_status, username

    def login(self, location: str = 'main',
              fields: dict = None,
              clear_on_submit: bool = False) -> tuple:
        """
        Crea un widget de inicio de sesión.

        Args:
            location (str): Ubicación del widget de inicio de sesión,
                            'main' o 'sidebar'.
            fields (dict): Nombres renderizados de los campos/botones.
            clear_on_submit (bool): Configuración de limpiar al enviar,
                                    True: limpia los campos al enviar,
                                    False: mantiene los campos al enviar.

        Returns:
            tuple: Nombre del usuario autenticado,
                   Estado de autenticación, None: no se ingresaron
                        credenciales,
                   False: credenciales incorrectas, True: credenciales
                        correctas,
                   Nombre de usuario autenticado.
        """
        if fields is None:
            fields = {'Form name': 'Inicio de sesión',
                      'Username': 'Nombre de usuario',
                      'Password': 'Contraseña',
                      'Login': 'Iniciar sesión'}

        if not st.session_state['authentication_status']:
            token = self.cookie_handler.get_cookie()
            if token:
                self.authentication_handler.execute_login(token=token)
            time.sleep(0.7)
            if not st.session_state['authentication_status']:
                if location == 'main':
                    login_form = st.form('Inicio de sesión',
                                         clear_on_submit=clear_on_submit)
                elif location == 'sidebar':
                    login_form = st.sidebar.form('Inicio de sesión')

                # Para el subencabezado del formulario
                if 'Form name' not in fields:
                    login_form.subheader('Iniciar sesión')
                else:
                    login_form.subheader(fields['Form name'])

                # Para el campo de entrada de texto del formulario
                # para el nombre de usuario
                if 'Username' not in fields:
                    username = (
                        login_form.text_input('Nombre de usuario').lower()
                    )
                else:
                    username = (
                        login_form.text_input(fields['Username']).lower()
                    )

                # Para el campo de entrada de texto del
                # formulario para la contraseña
                if 'Password' not in fields:
                    password = (
                        login_form.text_input('Contraseña', type='password')
                    )
                else:
                    password = (
                        login_form.text_input(fields['Password'],
                                              type='password')
                    )

                # Para el botón de envío del formulario
                if 'Login' not in fields:
                    login_button_clicked = (
                        login_form.form_submit_button('Iniciar sesión')
                    )
                else:
                    login_button_clicked = (
                        login_form.form_submit_button(fields['Login'])
                    )

                # Si el botón de envío del formulario se presiona, verifica
                # las credenciales y ejecuta el inicio de sesión
                if login_button_clicked:
                    if self.authentication_handler.check_credentials(username,
                                                                     password):
                        self.authentication_handler.execute_login(
                                                            username=username
                                                            )
                        self.cookie_handler.set_cookie()

        name = st.session_state['name']
        authentication_status = st.session_state['authentication_status']
        username = st.session_state['username']

        return name, authentication_status, username

    def logout(self, button_name: str = 'Cerrar sesión',
               location: str = 'main',
               key: Optional[str] = None):
        """
        Crea un botón de cierre de sesión.

        Args:
            button_name (str): Nombre renderizado del botón de cierre de
                sesión.
            location (str): Ubicación del botón de cierre de sesión,
                            'main', 'sidebar' o 'unrendered'.
            key (str): Clave única a utilizar en aplicaciones de varias
                páginas.

        Returns:
            None
        """
        if location not in ['main', 'sidebar', 'unrendered']:
            raise ValueError("Location debe ser uno de 'main', 'sidebar' o \
                             'unrendered'")
        if location == 'main':
            if st.button(button_name, key):
                # Actualizar el estado de inicio de sesión en la base de datos
                self.db.actualizar_estado_login(st.session_state['username'],
                                                False)
                self.authentication_handler.execute_logout()
                self.cookie_handler.delete_cookie()

        elif location == 'sidebar':
            if st.sidebar.button(button_name, key):
                # Actualizar el estado de inicio de sesión en la base de datos
                self.db.actualizar_estado_login(st.session_state['username'],
                                                False)
                self.authentication_handler.execute_logout()
                self.cookie_handler.delete_cookie()

        elif location == 'unrendered':
            if st.session_state['authentication_status']:
                # Actualizar el estado de inicio de sesión en la base de datos
                self.db.actualizar_estado_login(st.session_state['username'],
                                                False)
                self.authentication_handler.execute_logout()
                self.cookie_handler.delete_cookie()

    def register_user(self, location: str = 'main',
                      fields: dict = None) -> tuple:
        """
        Crea un widget para registrar un nuevo usuario.

        Args:
        - location (str): Ubicación del widget de registro de nuevo usuario,
                          'main' o 'sidebar'.
        - fields (dict): Nombres renderizados de los campos/botones.

        Returns:
        - tuple: Tupla con el correo electrónico, nombre de usuario y nombre
                 asociados al nuevo usuario.
        """

        if 'clear' not in st.session_state:
            st.session_state['clear'] = False

        clear_on_submit = st.session_state['clear']

        if fields is None:
            fields = {'Form name': 'Registrar usuario',
                      'Email': 'Correo electrónico',
                      'Username': 'Nombre de usuario',
                      'Password': 'Contraseña',
                      'Repeat password': 'Confirmar contraseña',
                      'Register': 'Registrar'}

        if location == 'main':
            register_user_form = st.form('Registrar usuario',
                                         clear_on_submit=clear_on_submit)
        elif location == 'sidebar':
            register_user_form = st.sidebar.form('Registrar usuario')

        # Para el subencabezado del formulario
        if 'Form name' not in fields:
            register_user_form.subheader('Registrar Usuario')
        else:
            register_user_form.subheader(fields['Form name'])

        # Para el campo de entrada de texto del formulario para el nombre
        if 'Nombre' not in fields:
            name = register_user_form.text_input('Nombre')
        else:
            name = register_user_form.text_input(fields['Nombre'])

        # Para el campo de entrada de texto del formulario para el
        # correo electrónico
        if 'Correo electrónico' not in fields:
            email = register_user_form.text_input('Correo electrónico')
        else:
            email = (
                register_user_form.text_input(fields['Correo electrónico'])
            )

        # Para el campo de entrada de texto del formulario
        # para el nombre de usuario
        if 'Nombre de usuario' not in fields:
            username = (
                register_user_form.text_input('Nombre de usuario').lower()
            )
        else:
            username = (
                register_user_form.text_input(
                    fields['Nombre de usuario']
                                             ).lower()
            )

        # Para el campo de entrada de texto del formulario para la contraseña
        if 'Contraseña' not in fields:
            password = (
                register_user_form.text_input('Contraseña', type='password')
            )
        else:
            password = (
                register_user_form.text_input(fields['Contraseña'],
                                              type='password')
            )

        # Para el campo de entrada de texto del formulario
        # para confirmar la contraseña
        if 'Confirmar contraseña' not in fields:
            password_r = (
                register_user_form.text_input('Confirmar contraseña',
                                              type='password')
            )
        else:
            password_r = (
                register_user_form.text_input(fields['Confirmar contraseña'],
                                              type='password')
            )

        # Para el botón de envío del formulario
        if 'Registrar' not in fields:
            register_button_clicked = (
                register_user_form.form_submit_button('Registrar')
            )
        else:
            register_button_clicked = (
                register_user_form.form_submit_button(fields['Registrar'])
            )

        username = username.lower()

        validate = self.validator.validate_registration_fields(name, email,
                                                               username,
                                                               password,
                                                               password_r)

        if self.authentication_handler.credentials_contains_value(email):
            st.error('El correo electrónico ya está registrado')
            return None, None, None, None

        elif username in self.authentication_handler.credentials['usernames']:
            st.error('El nombre de usuario ya está registrado')
            return None, None, None, None

        elif validate[0] is False:
            st.error(validate[1])
            return None, None, None, None

        if 'accepted' not in st.session_state:
            st.session_state['accepted'] = False

        if st.session_state['accepted'] is False:
            st.warning('Por favor, lea y acepte la política de tratamiento \
                        de datos personales para continuar')

        elif st.session_state['accepted'] is True:
            st.success('Política de tratamiento de datos personales aceptada. \
                        Pulse el botón de registro para continuar')

        expanded = not st.session_state['accepted']

        def on_change():
            st.session_state['accepted'] = not st.session_state['accepted']
            st.session_state['clear'] = not st.session_state['clear']

        with st.expander(':page_with_curl: Política de tratamiento de datos \
                         personales', expanded=expanded):
            self.tratamiento_datos()

            st.checkbox('Acepto la política de tratamiento de datos \
                        personales', value=st.session_state['accepted'],
                        on_change=on_change)

        if register_button_clicked and st.session_state['accepted'] is True:
            del st.session_state['accepted']
            del st.session_state['clear']
            return self.authentication_handler.register_user(password,
                                                             username,
                                                             name,
                                                             email)

        return None, None, None, None

    def reset_password(self, username: str, location: str = 'main',
                       fields: dict = None,
                       clear_on_submit: bool = False) -> bool:
        """
        Crea un widget para restablecer la contraseña.

        Args:
        - username (str): Nombre de usuario del usuario para
            restablecer la contraseña.
        - location (str): Ubicación del widget de restablecimiento
            de contraseña,
                          'main' o 'sidebar'.
        - fields (dict): Nombres renderizados de los campos/botones.
        - clear_on_submit (bool): Configuración de limpiar al enviar, True:
                                  limpia los campos al enviar, False: mantiene
                                  los campos al enviar.

        Returns:
        - bool: Estado del restablecimiento de la contraseña.
        """
        if fields is None:
            fields = {'Form name': 'Restablecer contraseña 🔑',
                      'Current password': 'Contraseña actual',
                      'New password': 'Nueva contraseña',
                      'Repeat password': 'Repetir contraseña',
                      'Reset': 'Restablecer'}

        if location == 'main':
            reset_password_form = st.form('Restablecer contraseña',
                                          clear_on_submit=clear_on_submit)
        elif location == 'sidebar':
            reset_password_form = st.sidebar.form('Restablecer contraseña')

        # Para el subencabezado del formulario
        if 'Form name' not in fields:
            form_name = 'Restablecer contraseña'
        else:
            form_name = fields['Form name']
        reset_password_form.subheader(form_name)

        # Para el campo de entrada de texto del formulario para
        # la contraseña actual
        if 'Current password' not in fields:
            current_password_field = 'Contraseña actual'
        else:
            current_password_field = fields['Current password']
        password = reset_password_form.text_input(
                                        current_password_field, type='password'
                                        )

        # Para el campo de entrada de texto del formulario
        # para la nueva contraseña
        if 'New password' not in fields:
            new_password_field = 'Nueva contraseña'
        else:
            new_password_field = fields['New password']
        new_password = reset_password_form.text_input(
                                            new_password_field, type='password'
                                            )

        # Para el campo de entrada de texto del formulario para
        # repetir la nueva contraseña
        if 'Repeat password' not in fields:
            repeat_password_field = 'Repetir contraseña'
        else:
            repeat_password_field = fields['Repeat password']
        new_password_repeat = reset_password_form.text_input(
                                        repeat_password_field, type='password'
                                            )

        # Para el botón de envío del formulario
        if 'Reset' not in fields:
            reset_button = 'Restablecer'
        else:
            reset_button = fields['Reset']
        if reset_password_form.form_submit_button(reset_button):
            hash_password = self.authentication_handler.reset_password(
                                                        username,
                                                        password,
                                                        new_password,
                                                        new_password_repeat)
            if hash_password:
                # Actualizar la constraseña en la base de datos
                self.db.actualizar_contrasena(username, hash_password)
                return True
        return None

    def update_user_details(self, username: str,
                            location: str = 'main',
                            fields: dict = None,
                            clear_on_submit: bool = False) -> bool:
        """
        Crea un widget para actualizar los detalles del usuario.

        Args:
        - username (str): Nombre de usuario del usuario para
            actualizar los detalles.
        - location (str): Ubicación del widget de actualización de
            detalles de usuario,
                          'main' o 'sidebar'.
        - fields (dict): Nombres renderizados de los campos/botones.
        - clear_on_submit (bool): Configuración de limpiar al enviar, True:
                                  limpia los campos al enviar, False: mantiene
                                  los campos al enviar.

        Returns:
        - bool: Estado de la actualización de los detalles del usuario.
        """
        if fields is None:
            fields = {'Form name': 'Actualizar detalles de usuario',
                      'Field': 'Campo', 'Name': 'Nombre',
                      'Email': 'Correo electrónico',
                      'New value': 'Nuevo valor',
                      'Update': 'Actualizar'}

        if location == 'main':
            update_user_details_form = st.form('Actualizar detalles de \
                                                usuario',
                                               clear_on_submit=clear_on_submit)
        elif location == 'sidebar':
            update_user_details_form = st.sidebar.form('Actualizar detalles \
                                                        de usuario')
        # Para el subencabezado del formulario
        if 'Form name' not in fields:
            form_name = 'Actualizar detalles de usuario'
        else:
            form_name = fields['Form name']

        update_user_details_form.subheader(form_name)

        # Convertir el nombre de usuario a minúsculas
        username = username.lower()

        # Para los campos del formulario para actualizar los
        # detalles del usuario
        if 'Name' not in fields:
            name_field = 'Nombre'
        else:
            name_field = fields['Name']
        if 'Email' not in fields:
            email_field = 'Correo electrónico'
        else:
            email_field = fields['Email']
        update_user_details_form_fields = [name_field, email_field]

        # Para el campo de selección del formulario
        if 'Field' not in fields:
            field_label = 'Campo'
        else:
            field_label = fields['Field']
        field = update_user_details_form.selectbox(
                                            field_label,
                                            update_user_details_form_fields
                                            )

        # Para el campo de entrada de texto del formulario para el nuevo valor
        if 'New value' not in fields:
            new_value_label = 'Nuevo valor'
        else:
            new_value_label = fields['New value']
        new_value = update_user_details_form.text_input(new_value_label)

        # Para determinar el campo a actualizar
        if update_user_details_form_fields.index(field) == 0:
            field = 'name'
        elif update_user_details_form_fields.index(field) == 1:
            field = 'email'

        # Para el botón de envío del formulario
        if 'Update' not in fields:
            update_button = 'Actualizar'
        else:
            update_button = fields['Update']
        if update_user_details_form.form_submit_button(update_button):
            if self.authentication_handler.update_user_details(new_value,
                                                               username,
                                                               field):
                self.cookie_handler.set_cookie()
                return True

    def tratamiento_datos(self):
        """
        Muestra la política de tratamiento de datos personales desde un
        archivo Markdown.

        Args:
            None

        Returns:
            None
        """

        with open("data/politica_datos.md", "r", encoding="utf-8") as file:
            policy = file.read()

        st.markdown(policy, unsafe_allow_html=True)
