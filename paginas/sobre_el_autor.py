"""
    Renderiza la sección de información del autor y contacto.
"""

# Importar librerías
import streamlit as st


def info_autor():
    st.markdown("# Sobre el autor")

    st.markdown(
        """
        ¡Hola! Mi nombre es **Anderson Bedoya Ciro** y soy estudiante de la
        Universidad Nacional de Colombia en Medellín.

        Como un apasionado de la programación y las motocicletas, he
        desarrollado **Wily MotoTrack** como un proyecto personal que entrelaza
        estas dos grandes pasiones. Mi objetivo es ofrecer una herramienta que
        ayude a motociclistas como yo a gestionar sus finanzas de manera
        eficiente y sencilla, mejorando así nuestra experiencia en el manejo
        diario de nuestras motocicletas y la economía que las rodea.

        ### Contacto
        Si tienes alguna pregunta, sugerencia o deseas colaborar en este
        proyecto, no dudes en ponerte en contacto conmigo. Estoy abierto a
        feedback y siempre busco mejorar la aplicación con nuevas ideas y
        perspectivas.

        ¡Gracias por tu interés en Wily MotoTrack! Para cualquier pregunta o
        sugerencia, no dudes en contactarme a través de mi correo electrónico
        [abedoyaci@unal.edu.co](mailto:abedoyaci@unal.edu.co) o visitar mis
        perfiles.
        """,
        unsafe_allow_html=False
    )

    st.markdown(
        """
        <table style="border-collapse: collapse;">
          <tr>
            <td style="border: none;"><a href="https://github.com/BluessyJazz"><img src="https://cdn.worldvectorlogo.com/logos/github-icon-2.svg" width="50" height="50"></a></td>
            <td style="border: none;"><a href="https://www.linkedin.com/in/anderson-bedoya-ciro-9abb1724a"><img src="https://cdn.worldvectorlogo.com/logos/linkedin-icon-2.svg" width="50" height="50"></a></td>
            <td style="border: none;"><a href="https://www.upwork.com/freelancers/~017adf9fda4a06cf8a"><img src="https://cdn.worldvectorlogo.com/logos/upwork-roundedsquare-1.svg" width="50" height="50"></a></td>
            <td style="border: none;"><a href="https://www.reddit.com/user/BluessyJazz/"><img src="https://cdn.worldvectorlogo.com/logos/reddit-4.svg" width="50" height="50"></a></td>
          </tr>
        </table>
        """,
        unsafe_allow_html=True
    )
