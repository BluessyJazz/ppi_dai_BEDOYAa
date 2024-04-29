"""
Este módulo contiene la implementación de los menús de la aplicación
utilizando Streamlit.
"""

# Importar os para eliminar archivos temporales
import os
# Importar re para expresiones regulares
import re
# Importar time para pausar la ejecución
import time
# Importar streamlit
import streamlit as st
# Importar librería para menús
from streamlit_option_menu import option_menu
# Importar páginas locales
from paginas.bienvenida import pagina_bienvenida
from paginas.sobre_el_autor import info_autor
from modules.auth.auth_utils import AuthUtils
from modules.db.user_repository import UserRepository


class Menu:
    """
    Clase para los menús de la aplicación.
    """

    def __init__(self):
        """Inicializa la clase Menu."""

    def land_page(self):
        """
        Muestra la página de inicio de la aplicación.
        """

        # Cargar menú en la barra lateral
        with st.sidebar:
            selected = option_menu(
                None,
                ["Wily MotoTrack", "Iniciar Sesión", "Registrate",
                 "Prueba la app", "Sobre el autor"],
                icons=["speedometer2", "box-arrow-in-right", "pencil-square",
                       "play-circle", "person-lines-fill"],
                menu_icon="cast",
                default_index=0
            )

        # Mostrar la página seleccionada
        if selected == 'Wily MotoTrack':

            pagina_bienvenida()

        elif selected == 'Iniciar Sesión':

            self.login_page()

        elif selected == 'Registrate':

            self.register_page()

        elif selected == 'Prueba la app':

            st.title("Pronto podrás usar la aplicación")

        elif selected == 'Sobre el autor':

            info_autor()

    def user_page(self):
        """
        Muestra la página de inicio de la aplicación.
        """

        # Inicializar AuthUtils
        auth_utils = AuthUtils()

        # Autenticar al usuario
        authenticator = auth_utils.authenticate()

        # Eliminar el archivo de configuración temporal
        os.remove('temp_config.yaml')

        # Cargar menú en la barra lateral
        with st.sidebar:
            selected = option_menu(
                None,
                ["Wily MotoTrack", "Sobre el autor"],
                icons=["speedometer2", "person-lines-fill"],
                menu_icon="cast",
                default_index=0
            )

            # Mostrar el botón de cierre de sesión
            if authenticator.logout(button_name="Cerrar Sesión"):
                st.session_state["authentication_status"] = False

        # Mostrar la página seleccionada          
        if selected == 'Wily MotoTrack':

            pagina_bienvenida()

        elif selected == 'Sobre el autor':

            info_autor()

    def login_page(self):
        """
        Muestra el menú de la inicio de sesión.
        """

        # Inicializar AuthUtils
        auth_utils = AuthUtils()

        # Autenticar al usuario
        authenticator = auth_utils.authenticate()

        # Mostrar menú de autenticación
        campos = {
            'Form name': 'Iniciar Sesión',
            'Username': 'Usuario',
            'Password': 'Contraseña',
            'Login': 'Ingresar'
        }

        # Autenticar al usuario
        authenticator.login(fields=campos)

        # Mostrar mensaje de autenticación
        if st.session_state["authentication_status"]:
            st.title("Iniciando sesión...")

        # Mostrar mensaje de error
        else:
            if st.session_state["authentication_status"] is None:
                st.warning('Por favor ingresa tu usuario y contraseña')
            elif st.session_state["authentication_status"] is False:
                st.error('Usuario o contraseña incorrectos')

            st.markdown("""
                        Si no tienes una cuenta, puedes
                        [registrarte](/Registro).
                        """)

        # Eliminar el archivo de configuración temporal            
        os.remove('temp_config.yaml')

    def register_page(self):
        """
        Muestra el menú de registro de usuarios.
        """

        # Instancia del repositorio de usuarios
        user_repo = UserRepository()

        # Inicializar variables de sesión
        if 'registrado' not in st.session_state:
            st.session_state.registrado = False
        if 'usuario' not in st.session_state:
            st.session_state.usuario = False

        if st.session_state.registrado is False:
            
            # Solicitar al usuario que introduzca sus datos
            nombre = st.text_input("Nombre")
            correo = st.text_input("Correo")
            usuario = st.text_input("Usuario")
            contrasena = st.text_input("Contraseña", type="password")
            confirma_contrasena = st.text_input("Confirma tu contraseña",
                                                type="password")

            # Convertir el usuario a minúsculas
            usuario = usuario.lower()

            # Verificar si el usuario ya existe
            existente = user_repo.verify_user(usuario, correo)
            campos_correctos = self.verificar_campos(nombre, correo, 
                                                     usuario, contrasena,
                                                     confirma_contrasena)

            if not existente and campos_correctos:
                st.warning("Debes leer y aceptar la política de \
                            tratamiento de datos personales para continuar.")
                self.tratamiento_datos()
                acepta_politicas = st.checkbox("Acepto la política de \
                                                tratamiento de datos \
                                                personales")

                boton_registrar = st.button("Registrarme")

                if boton_registrar and acepta_politicas:
                    st.write("Registrando usuario...")

                    registrado = user_repo.create_user(nombre, correo,
                                                       usuario,
                                                       contrasena,
                                                       'usuario') > 0

                    if registrado:
                        st.success("Usuario registrado con éxito!")
                    else:
                        st.error("Ha ocurrido un error al registrar \
                                 el usuario. Por favor, inténtalo de nuevo.")

                    st.session_state.usuario = usuario
                    st.session_state.registrado = True

                    time.sleep(2)
                    st.rerun()

        else:
            st.title("Ya tienes tu cuenta en la app! 👏🎉")
            st.write(f"""
                        Puedes iniciar sesión como 
                        **{st.session_state.usuario}**
                        en el menú lateral ⬅️.
                        """)
            st.session_state.registrado = False

    def is_valid_email(self, email):
        """
        Verifica si un correo electrónico es válido.

        Args:
            email (str): El correo electrónico a verificar.

        Returns:
            bool: True si el correo es válido, False en caso contrario.
        """

        pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return bool(pattern.match(email))

    def is_password_strong(self, password):
        """
        Verifica si la contraseña es segura.
        Retorna un mensaje indicando el problema si la contraseña no es segura.
        Retorna 'ok' si la contraseña cumple todos los criterios.
        """
        if " " in password:
            return "La contraseña no puede contener espacios."
        if len(password) < 8:
            return "La contraseña debe tener al menos 8 caracteres."
        if not re.search("[a-z]", password):
            return "La contraseña debe contener al menos una letra minúscula."
        if not re.search("[A-Z]", password):
            return "La contraseña debe contener al menos una letra mayúscula."
        if not re.search("[0-9]", password):
            return "La contraseña debe contener al menos un dígito numérico."
        if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
            return "La contraseña debe contener al menos un símbolo especial \
                    (ej. !@#$%^&*(),.?\":{}|<>)."
        return "ok"

    def verificar_campos(self, nombre, correo, usuario, 
                         contrasena, confirma_contrasena):
        """
        Verifica si los campos de registro del usuario
        están correctos.
        """

        if not nombre:
            st.error("Por favor, introduce tu nombre.")
            return False
        if not correo:
            st.error("Por favor, introduce tu correo electrónico.")
            return False
        if not self.is_valid_email(correo):
            st.error("Por favor, introduce un correo electrónico válido.")
            return False
        if not usuario:
            st.error("Por favor, introduce tu nombre de usuario.")
            return False
        if " " in usuario:
            st.error("El nombre de usuario no puede contener espacios.")
            return False
        if not contrasena:
            st.error("Por favor, introduce tu contraseña.")
            return False
        if not confirma_contrasena:
            st.error("Por favor, confirma tu contraseña.")
            return False
        if contrasena != confirma_contrasena:
            st.error("Las contraseñas no coinciden. Por favor, \
                        inténtalo de nuevo.")
            return False
        if self.is_password_strong(contrasena) != "ok":
            st.error(self.is_password_strong(contrasena))
            return False

        return True

    def tratamiento_datos(self):
        """
        Muestra la política de tratamiento de datos
        personales desde un archivo Markdown.
        """

        with open("data/politica_datos.md", "r", encoding="utf-8") as file:
            policy = file.read()

        st.markdown(policy, unsafe_allow_html=True)
