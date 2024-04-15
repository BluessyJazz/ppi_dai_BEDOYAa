"""
Página de inicio de sesión
"""

import time
import psycopg2
import streamlit as st
from streamlit import session_state
import sys
sys.path.append('./modules')  # Replace '/path/to/modules' with the actual path
                                #to the 'modules' directory
from modules.db.crear_usuario import crear_usuario
from modules.db.conexion_db import conectar_db

# Configuración de la página
st.set_page_config(page_title="Iniciar Sesión", page_icon="🔒")

# Verificar si el usuario ha iniciado sesión
if 'login' not in st.session_state:
    st.session_state.login = False

# Conexión a la base de datos
conn = conectar_db()

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
            del session_state.username
            st.success("Has cerrado sesión exitosamente.")
            time.sleep(2)  # Esperar dos segundos
            st.experimental_rerun()  # Recargar la página

else:
    # Si el usuario no ha iniciado sesión, mostrar la página de
    # inicio de sesión

    # Título de la página
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
                st.success("Hola {}!".format(session_state.username))
                time.sleep(2)  # Esperar dos segundos
                st.experimental_rerun()  # Recargar la página
            else:
                st.write("Por favor inicia sesión para continuar.")

            cursor.close()

    
