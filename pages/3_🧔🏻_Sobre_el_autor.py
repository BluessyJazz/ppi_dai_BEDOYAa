"""
    Renderiza la sección de información del autor y contacto.
"""

import streamlit as st

st.set_page_config(page_title="Sobre el autor", page_icon="🧔🏻")

st.markdown("# Sobre el autor")

st.markdown(
    """
    ¡Hola! Mi nombre es **Anderson Bedoya Ciro** y soy estudiante de la Universidad Nacional de Colombia en Medellín, donde combino mi interés por la tecnología y las finanzas.

    Como un apasionado de la programación y las motocicletas, he desarrollado **Wily MotoTrack** como un proyecto personal que entrelaza estas dos grandes pasiones. Mi objetivo es ofrecer una herramienta que ayude a motociclistas como yo a gestionar sus finanzas de manera eficiente y sencilla, mejorando así nuestra experiencia en el manejo diario de nuestras motocicletas y la economía que las rodea.

    ### Contacto
    Si tienes alguna pregunta, sugerencia o deseas colaborar en este proyecto, no dudes en ponerte en contacto conmigo. Estoy abierto a feedback y siempre busco mejorar la aplicación con nuevas ideas y perspectivas.

    - **Correo Electrónico:** [abedoyaci@unal.edu.co](mailto:abedoyaci@unal.edu.co)
    - **LinkedIn:** [Visita mi perfil aquí](https://www.linkedin.com/in/anderson-bedoya-ciro-9abb1724a)

    Agradezco tu interés en Wily MotoTrack y espero que la encuentres tan útil y emocionante como yo al crearla.

    """
)