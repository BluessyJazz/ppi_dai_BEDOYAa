"""
Wily MotoTrack - Aplicación para el registro de
gastos e ingresos de motociclistas.

Este módulo contiene la implementación de la aplicación principal
utilizando Streamlit.
"""

import streamlit as st


st.set_page_config(
    page_title="Wily MotoTrack",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.write("# Bienvenido a Wily MotoTrack! 👋")

st.write("## ¿Qué es Wily MotoTrack? 🏍️")

st.markdown(
    """
    Wily MotoTrack es una aplicación para el registro de gastos e ingresos
    de motociclistas. Con esta aplicación, los usuarios pueden llevar un
    registro detallado de sus gastos y ganancias relacionados con su
    motocicleta.
    """
)

st.write("## ¿Por qué usar Wily MotoTrack? 🤔")

st.markdown(
    """
    - **Registro de Gastos:** Lleva un registro detallado de tus gastos
    relacionados con tu motocicleta.
    - **Registro de Ingresos:** Registra tus ingresos y ganancias obtenidas
    con tu motocicleta.
    - **Análisis de Datos:** Visualiza y analiza tus datos de gastos e
    ingresos para tomar decisiones informadas.
    - **Fácil de Usar:** Interfaz sencilla e intuitiva para una mejor
    experiencia de usuario.
    """
)

st.write("## ¿Cómo funciona? 🚀")

st.markdown(
    """
    1. **Iniciar Sesión:** Regístrate e inicia sesión en la aplicación.
    2. **Registrar Gastos:** Registra tus gastos relacionados con tu
    motocicleta.
    3. **Registrar Ingresos:** Registra tus ingresos y ganancias obtenidas
    con tu motocicleta.
    4. **Visualizar Datos:** Visualiza y analiza tus datos de gastos e
    ingresos en gráficos interactivos.
    """
)

st.write("## ¿Listo para comenzar? 🚦")

st.markdown(
    """
    ¡Selecciona una opción del menú lateral para comenzar!
    """
)
