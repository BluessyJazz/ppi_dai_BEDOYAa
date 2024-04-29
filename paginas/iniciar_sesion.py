"""
Página de inicio de sesión
"""

# Importar librerías para 
import streamlit as st

# Importar módulos
from modules.menus import Menu

# Configuración de la página
st.set_page_config(page_title="Iniciar Sesión", page_icon="🔒")

# Inicializar el menú
menu = Menu()

# Mostrar el menú de inicio de sesión
menu.login_page()
