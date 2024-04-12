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

def author_info():
    """
    Renderiza la sección de información del autor y contacto.
    """
    st.sidebar.title("Sobre el Autor")
    st.sidebar.markdown("""
    **Anderson Bedoya Ciro**
    **Correo Electrónico:** abedoyaci@unal.edu.co
    
    Soy un entusiasta programación y las motocicletas. Esta aplicación es un proyecto
    personal que combina estas dos pasiones. Si tienes alguna pregunta o sugerencia, no dudes
    en ponerte en contacto conmigo.
    """)

def main():
    """
    Función principal que maneja la navegación y el enrutamiento de páginas.
    """
    # Página de navegación
    st.sidebar.title("Navegación")
    page = st.sidebar.radio("Ir a", ["Página Principal", "Iniciar Sesión", "Sobre el Autor"])

    if page == "Página Principal":
        main_page()
    elif page == "Iniciar Sesión":
        login_page()
    elif page == "Sobre el Autor":
        author_info()

if __name__ == "__main__":
    main()
