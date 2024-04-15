"""
Página de inicio de sesión
"""


import pymysql
import streamlit as st
from streamlit import session_state
import time

# Configuración de la página
st.set_page_config(page_title="Iniciar Sesión", page_icon="🔒")

# Título de la página
st.markdown("# Inicio de Sesión")

# Verificar si el usuario ha iniciado sesión
if 'login' not in st.session_state:
    st.session_state.login = False

# Conexión a la base de datos
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='daker2002',
    database='wilymoto'
)

# Formulario de inicio de sesión
if not st.session_state.login:
    login_form = st.form("login_form")
    username = login_form.text_input("Usuario")
    password = login_form.text_input("Contraseña", type="password")

    if login_form.form_submit_button("Iniciar Sesión"):
        cursor = conn.cursor()
        QUERY = "SELECT * FROM usuarios WHERE nombre=%s AND contraseña=%s"
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

        conn.close()

# Cerrar sesión
if st.session_state.login:
    if st.button("Cerrar sesión"):
        st.session_state.login = False
        del session_state.username
        st.succes("Has cerrado sesión exitosamente.")
        time.sleep(2)  # Esperar dos segundos
        st.experimental_rerun()  # Recargar la página
