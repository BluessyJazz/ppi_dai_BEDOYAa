"""
Wily MotoTrack - Aplicación para el registro de
gastos e ingresos de motociclistas.

Este módulo contiene la implementación de la aplicación principal
utilizando Streamlit.
"""

# Importar librerías
# - streamlit: Para la interfaz web
import streamlit as st

# Importar módulos locales
# - menu: Para mostrar el menú de la aplicación en la barra lateral
from menu import menu

# Configuración de la página
st.set_page_config(
    page_title="Inicio · Wily MotoTrack",
    page_icon="🏍️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Pestañas de la página
tab1, tab2 = st.tabs(["Inicio", "Acerca de 🧔🏻"])

# Contenido de la pestaña de inicio
with tab1:
    st.markdown(
        """
        # Bienvenido a Wily MotoTrack! 👋

        ## ¿Qué es Wily MotoTrack? 🏍️

        Wily MotoTrack es una aplicación para el registro de gastos e ingresos
        de motociclistas. Con esta aplicación, los usuarios pueden llevar un
        registro detallado de sus gastos y ganancias relacionados con su
        motocicleta.

        ## ¿Por qué usar Wily MotoTrack? 🤔

        - **Registro de Gastos:** Lleva un registro detallado de tus gastos
        relacionados con tu motocicleta.
        - **Registro de Ingresos:** Registra tus ingresos y ganancias obtenidas
        con tu motocicleta.
        - **Análisis de Datos:** Visualiza y analiza tus datos de gastos e
        ingresos para tomar decisiones informadas.
        - **Fácil de Usar:** Interfaz sencilla e intuitiva para una mejor
        experiencia de usuario.

        ## ¿Cómo funciona? 🚀

        1. **Iniciar Sesión:** Regístrate e inicia sesión en la aplicación.
        2. **Registrar Gastos:** Registra tus gastos relacionados con tu
        motocicleta.
        3. **Registrar Ingresos:** Registra tus ingresos y ganancias obtenidas
        con tu motocicleta.
        4. **Visualizar Datos:** Visualiza y analiza tus datos de gastos e
        ingresos en gráficos interactivos.

        ## ¿Listo para comenzar? 🚦

        ¡Selecciona una opción del menú lateral para comenzar!
        """,
        unsafe_allow_html=True
    )

with tab2:

    st.markdown(
        """
        # Sobre el autor

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

        <table style="border-collapse: collapse;">
        <tr>
            <td style="border: none;"><a href="https://www.linkedin.com/in/anderson-bedoya-ciro-9abb1724a"><img src="https://cdn.worldvectorlogo.com/logos/linkedin-icon-2.svg" alt="LinkedIn" width="50" style="margin-right: 20px;"></a></td>
            <td style="border: none;"><a href="https://golance.com/freelancer/anderson.bedoya.ciro"><img src="https://res-1.cloudinary.com/golance/image/upload/q_auto:good/v1/blog_staging/icon-round-white-BG.svg" alt="goLance" width="50" style="margin-right: 20px;"></a></td>
            <td style="border: none;"><a href="https://www.upwork.com/freelancers/~017adf9fda4a06cf8a"><img src="https://cdn.worldvectorlogo.com/logos/upwork-roundedsquare-1.svg" alt="Upwork" width="50" style="margin-right: 20px;"></a></td>
            <td style="border: none;"><a href="https://www.freelancer.com/u/bluessyjazz"><img src="https://cdn.worldvectorlogo.com/logos/freelancer-1.svg" alt="Freelancer" width="50" style="margin-right: 20px;"></a></td>
            <td style="border: none;"><a href="https://github.com/BluessyJazz"><img src="https://cdn.worldvectorlogo.com/logos/github-icon-2.svg" alt="GitHub" width="50" style="margin-right: 20px;"></a></td>
            <td style="border: none;"><a href="https://stackoverflow.com/users/24114620/anderson-bedoya-ciro"><img src="https://cdn.worldvectorlogo.com/logos/stack-overflow.svg" alt="Stack Overflow" width="50" style="margin-right: 20px;"></a></td>
            <td style="border: none;"><a href="https://www.reddit.com/user/BluessyJazz/"><img src="https://cdn.worldvectorlogo.com/logos/reddit-4.svg" alt="Reddit" width="50" style="margin-right: 20px;"></a></td>
            <td style="border: none;"><a href="https://buymeacoffee.com/bluessyjazz"><img src="https://studio.buymeacoffee.com/assets/img/qr-logo.svg" alt="Buy Me a Coffee" width="50" style="margin-right: 20px;"></a></td>
        </tr>
        </table>
        """,
        unsafe_allow_html=True
    )

if ('authentication_status' not in st.session_state or
   not st.session_state['authentication_status']):
    menu(auth=None)

else:
    auth = st.session_state.get('auth', None)
    menu(auth)
