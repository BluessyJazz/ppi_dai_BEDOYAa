"""
Este módulo contiene la implementación de la página de registro de usuarios

"""

import sys
sys.path.append('./modules')  # Replace '/path/to/modules' with the actual path
                                #to the 'modules' directory
import streamlit as st
from modules.db.conexion_db import conectar_db
from modules.db.verificar_usuario import verificar_usuario
from modules.db.crear_usuario import crear_usuario

st.set_page_config(page_title="Registro", page_icon="👤")

st.markdown("# Registro de Usuarios")

# Solicitar al usuario que introduzca sus datos
nombre = st.text_input("Nombre de usuario")
correo = st.text_input("Correo electrónico")
contrasena = st.text_input("Contraseña", type="password")
boton_registrar = st.button("Registrar")

# Verificar las credenciales del usuario y crear el usuario si no existe
if boton_registrar:
    if verificar_usuario(nombre, correo):
        st.warning("El nombre de usuario o correo electrónico ya está en uso.\
                    Por favor, elige otro.")
    else:
        crear_usuario(nombre, correo, contrasena)
        st.success("Usuario registrado con éxito!")