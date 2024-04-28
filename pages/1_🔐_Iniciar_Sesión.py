"""
Página de inicio de sesión
"""

# Importar librerías
import time
import streamlit as st

# Importar módulos
from modules.db.user_repository import UserRepository

# Configuración de la página
st.set_page_config(page_title="Iniciar Sesión", page_icon="🔒")

# Inicializar la conexión a la base de datos y el repositorio
user_repo = UserRepository()

# Verificar si el usuario ha iniciado sesión
if 'login' not in st.session_state:
    # Inicializar la variable de sesión
    st.session_state.login = False

# Verificar si el usuario ya ha iniciado sesión
if st.session_state.get('login', False):
    # Si el usuario ya ha iniciado sesión, redirigirlo a otra
    # página o simplemente no mostrar nada
    st.markdown("# Bienvenido de nuevo!")
    st.markdown("""
                Ya has iniciado sesión, por lo que no necesitas
                hacerlo de nuevo.
                """)

    # Cerrar sesión
    if st.session_state.login:
        if st.button("Cerrar sesión"):
            st.session_state.login = False
            del st.session_state.username
            st.success("Has cerrado sesión exitosamente.")
            time.sleep(2)
            st.rerun()

else:
    # Si el usuario no ha iniciado sesión, mostrar la página de
    # inicio de sesión

    # Crear titulo de la página
    st.markdown("# Inicio de Sesión")

    # Formulario de inicio de sesión
    if not st.session_state.login:
        login_form = st.form("login_form")
        username = login_form.text_input("Usuario")
        password = login_form.text_input("Contraseña", type="password")

        if login_form.form_submit_button("Iniciar Sesión"):
            if user_repo.verify_user(username, password):
                st.session_state.login = True
                st.session_state.username = username
                st.success(f"Hola {st.session_state.username}!")
                time.sleep(2)
                st.rerun()
            else:
                st.warning("Credenciales inválidas")
                st.markdown("""
                            Si no tienes una cuenta, puedes
                            [registrarte](/Registro).
                            """)
