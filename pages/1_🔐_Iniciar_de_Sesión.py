"""
Página de inicio de sesión
"""

# Importar librerías
import time  # Para simular un tiempo de espera
import sys  # Para poder importar módulos de otros directorios
import streamlit as st  # Para la interfaz web
from streamlit import session_state  # Para manejar el estado de la sesión

sys.path.append('./modules')  # Agregar el directorio modules al path

# Para la conexión a la base de datos
from modules.db.conexion_db import conectar_db

# Configuración de la página
st.set_page_config(page_title="Iniciar Sesión", page_icon="🔒")

# Verificar si el usuario ha iniciado sesión
if 'login' not in st.session_state:
    st.session_state.login = False  # Inicializar la variable de sesión

# Conexión a la base de datos
conn = conectar_db()

# Verificar si el usuario ya ha iniciado sesión
if st.session_state.get('login', False):
    # Si el usuario ya ha iniciado sesión, redirigirlo a otra
    # página o simplemente no mostrar nada
    st.markdown("# Bienvenido de nuevo!")  # Mensaje de bienvenida
    st.markdown("""
                Ya has iniciado sesión, por lo que no necesitas
                hacerlo de nuevo.
                """)  # Mensaje de información

    # Cerrar sesión
    if st.session_state.login:  # Si el usuario ha iniciado sesión
        if st.button("Cerrar sesión"):  # Botón para cerrar sesión
            st.session_state.login = False  # Cerrar la sesión
            del session_state.username  # Eliminar el nombre de usuario
            st.success("Has cerrado sesión exitosamente.")  # Mensaje de éxito
            time.sleep(2)  # Esperar dos segundos
            st.rerun()  # Recargar la página

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
            cursor = conn.cursor()
            QUERY = "SELECT * FROM usuarios WHERE nombre=%s AND contrasena=%s"
            values = (username, password)
            cursor.execute(QUERY, values)
            record = cursor.fetchone()

            if record:
                st.session_state.login = True
                session_state.username = username
            else:
                st.warning("Credenciales inválidas")

            if st.session_state.login:
                st.success(f"Hola {session_state.username}!")
                time.sleep(2)  # Esperar dos segundos
                st.rerun()  # Recargar la página
            else:
                st.write("""
                            Por favor inicia
                            sesión para continuar.
                        """)  # Mensaje de información

            cursor.close()
