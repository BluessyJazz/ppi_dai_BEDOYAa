"""
Este módulo contiene la implementación de la página de registro de usuarios

"""

import streamlit as st
# from modules.db.conexion_db import insertar_usuario

st.set_page_config(page_title="Iniciar Sesión", page_icon="👤")

st.markdown("# Registro de Usuarios")

nombre = st.text_input("Nombre")
correo = st.text_input("Correo Electrónico")
contrasena = st.text_input("Contraseña", type="password")

if st.button("Registrarse"):
    if nombre and correo and contrasena:
        # Insertar usuario en la base de datos
        #insertar_usuario(nombre, correo, contrasena)
        st.success("¡Registro exitoso! Por favor inicia sesión.")
    else:
        st.error("Por favor completa todos los campos.")