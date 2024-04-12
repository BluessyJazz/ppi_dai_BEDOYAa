# app.py
import streamlit as st


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


def main():
    """
    Función principal que maneja la navegación y el enrutamiento de páginas.
    """
    # Página de navegación
    st.sidebar.title("Navegación")
    page = st.sidebar.selectbox("Ir a", ["Página Principal", "Iniciar Sesión"])

    if page == "Página Principal":
        main_page()
    elif page == "Iniciar Sesión":
        login_page()

if __name__ == "__main__":
    main()
