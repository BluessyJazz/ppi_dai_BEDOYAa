"""
Este módulo contiene la implementación de la página de inicio de sesión
"""

import streamlit as st

st.set_page_config(page_title="Iniciar Sesión", page_icon="🔒")

st.markdown("# Inicio de Sesión")

with st.form("login_form"):
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    submitted = st.form_submit_button("Iniciar Sesión")
    if submitted:
        if username == "admin" and password == "password":
            st.success("Inicio de sesión exitoso")
        else:
            st.error("Credenciales inválidas")
