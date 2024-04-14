"""
    Renderiza la sección de información del autor y contacto.
"""

import streamlit as st

st.set_page_config(page_title="Sobre el autor", page_icon="🧔🏻")

st.markdown("# Anderson Bedoya Ciro")

st.markdown(
    """
    **Anderson Bedoya Ciro**

    abedoyaci@unal.edu.co

    Soy un entusiasta de la programación y las motocicletas. Esta aplicación
    es un proyecto personal que combina estas dos pasiones. Si tienes alguna
    pregunta o sugerencia, no dudes en ponerte en contacto conmigo.
    """
)