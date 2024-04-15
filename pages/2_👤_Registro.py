"""
Este módulo contiene la implementación de la página de registro de usuarios
"""

# Importar librerías
import sys  # Para poder importar módulos de otros directorios
import streamlit as st  # Para la interfaz web

# Configuración de path para importaciones de módulos
sys.path.append('./modules')

# Importaciones locales
from modules.db.conexion_db import conectar_db  # Para la conexión a la base de datos
from modules.db.verificar_usuario import verificar_usuario  # Para verificar si el usuario ya existe
from modules.db.crear_usuario import crear_usuario  # Para crear un nuevo usuario

# Configuración inicial de la página de Streamlit
st.set_page_config(page_title="Registro", page_icon="👤")

st.markdown("# Registro de Usuarios")

# Solicitar al usuario que introduzca sus datos
nombre = st.text_input("Nombre de usuario")  # Campo para el nombre de usuario
correo = st.text_input("Correo electrónico")  # Campo para el correo electrónico
contrasena = st.text_input("Contraseña", type="password")  # Campo para la contraseña
boton_registrar = st.button("Registrar")  # Botón para registrar al usuario

# Verificar las credenciales del usuario y crear el usuario si no existe
if boton_registrar:
    if verificar_usuario(nombre, correo):
        st.warning("""
                    El nombre de usuario o correo electrónico ya
                    está en uso. Por favor, elige otro.
                    """)
    else:
        crear_usuario(nombre, correo, contrasena)
        st.success("Usuario registrado con éxito!")
