"""
Este módulo contiene la implementación de la página de registro de usuarios
"""

# Importaciones locales
from modules.db.user_repository import UserRepository

# Importar librerías
import streamlit as st


# Configuración inicial de la página de Streamlit
st.set_page_config(page_title="Registro", page_icon="👤")

# Dar titulo a la página
st.markdown("# Registro de Usuarios")

# Instancia del repositorio de usuarios
user_repo = UserRepository()

# Solicitar al usuario que introduzca sus datos
nombre = st.text_input("Nombre de usuario")
correo = st.text_input("Correo electrónico")
contrasena = st.text_input("Contraseña", type="password")
boton_registrar = st.button("Registrar")

# Verificar las credenciales del usuario y crear el usuario si no existe
if boton_registrar:
    if user_repo.verify_user(nombre, correo):
        st.warning("""
                    El nombre de usuario o correo electrónico ya
                    está en uso. Por favor, elige otro.
                    """)
    else:
        registrado = user_repo.create_user(nombre, correo,
                                           contrasena, 'usuario') > 0
        if registrado:
            st.success("Usuario registrado con éxito!")
        else:
            st.error("Ha ocurrido un error al registrar el usuario. \
                     Por favor, inténtalo de nuevo.")
