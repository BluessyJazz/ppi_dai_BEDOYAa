"""
Wily MotoTrack - Aplicación para el registro de
gastos e ingresos de motociclistas.

Este módulo contiene la implementación de la aplicación principal
utilizando Streamlit.
"""

import streamlit as st
from modules.db.conexion_db import insertar_usuario

st.set_page_config(
    page_title="Wily MotoTrack",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main_page():
    """
    Renderiza la página principal de la aplicación.
    """
    st.title("Bienvenido a Wily MotoTrack")


def login_page():
    """
    Renderiza la página de inicio de sesión.
    """
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar Sesión")
        if submitted:
            if username == "admin" and password == "password":
                st.success("Inicio de sesión exitoso")
            else:
                st.error("Credenciales inválidas")


def registro_usuario():
    """
    Renderiza el formulario de registro de usuarios y gestiona la inserción
    en la base de datos.
    """
    st.title("Registro de Usuarios")

    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo Electrónico")
    contrasena = st.text_input("Contraseña", type="password")

    if st.button("Registrarse"):
        if nombre and correo and contrasena:
            # Insertar usuario en la base de datos
            insertar_usuario(nombre, correo, contrasena)
            st.success("¡Registro exitoso! Por favor inicia sesión.")
        else:
            st.error("Por favor completa todos los campos.")


def author_info():
    """
    Renderiza la sección de información del autor y contacto.
    """
    st.sidebar.title("Sobre el Autor")
    st.sidebar.markdown("""
    **Anderson Bedoya Ciro**
    abedoyaci@unal.edu.co

    Soy un entusiasta de la programación y las motocicletas. Esta aplicación
    es un proyecto personal que combina estas dos pasiones. Si tienes alguna
    pregunta o sugerencia, no dudes en ponerte en contacto conmigo.
    """)


def main():
    """
    Función principal que maneja la navegación y el enrutamiento de páginas.
    """
    # Página de navegación
    st.sidebar.title("Navegación")
    page = st.sidebar.radio("Ir a", ["Página Principal",
                                     "Iniciar Sesión",
                                     "Crear Cuenta",
                                     "Sobre el Autor"])

    if page == "Página Principal":
        main_page()
    elif page == "Iniciar Sesión":
        login_page()
    elif page == "Crear Cuenta":
        registro_usuario()
    elif page == "Sobre el Autor":
        author_info()


if __name__ == "__main__":
    main()
