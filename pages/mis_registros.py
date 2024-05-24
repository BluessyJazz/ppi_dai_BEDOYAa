"""
Este script se encarga de visualizar los registros financieros de un usuario.
Se conecta a la base de datos para obtener los registros financieros y
permite al usuario modificar o eliminar registros existentes.
"""

# Importar librerías
# - time: Para pausar la ejecución del script
# - streamlit: Para la interfaz web
# - pandas: Para trabajar con DataFrames
# - datetime: Para obtener la fecha y hora actuales
import time
import pandas as pd
from datetime import datetime
import streamlit as st

# Importar módulos locales
# - menu: Para mostrar el menú de la aplicación en la barra lateral
# - init_auth: Para inicializar la autenticación
# - ConexionDB: Para conectarse a la base de datos
from menu import menu
from modules.auth import init_auth
from modules.db import ConexionDB

# Configuración de la página
st.set_page_config(
    page_title="Mis Registros · Wily MotoTrack",
    page_icon="🏍️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Título de la página
st.title("Mis Registros")

# Inicializar la autenticación
auth = init_auth()

# Autenticar al usuario
if auth.login_with_cookie():
    pass

# Si el usuario no está autenticado, mostrar el menú sin autenticación
if (
    "authentication_status" not in st.session_state
    or not st.session_state["authentication_status"]
):
    st.write("Por favor inicia sesión para ver esta página.")
    menu(auth=None)
    st.stop()

# Si el usuario está autenticado, mostrar el menú
else:
    menu(auth)

# Crear una instancia de la conexión a la base de datos
db = ConexionDB()

# Obtener el ID del usuario
user_id = st.session_state.get('user_id')

# Consultar los registros financieros del usuario
resultados = db.obtener_registro_financiero(user_id)

if resultados:
    # Crear un DataFrame con los registros financieros
    df = pd.DataFrame(resultados, columns=["ID", "Actividad", "Tipo", "Monto",
                                           "Descripción", "Fecha"])

    # Establecer el ID como índice
    df.set_index("ID", inplace=True)

    # Guardar el DataFrame en el estado de la sesión
    st.session_state.df = df    

    if 'df' in st.session_state and not st.session_state.df.empty:
        df = st.session_state.df

        # Opción de selección para ordenar el DataFrame
        orden = st.selectbox('Ordenar por', options=['ID', 'Fecha'])

        if orden == 'ID':
            df.sort_index(inplace=True)
        elif orden == 'Fecha':
            df.sort_values(by='Fecha', inplace=True)

        # Mostrar los registros financieros
        st.subheader("Registros Financieros")
        st.write(df)

    # Crear un expander para modificar registros
    with st.expander("Modificar un registro"):
        # Crear un formulario para modificar registros
        with st.form(key='modificar_form'):
            df = st.session_state.df
            registro = st.number_input('Ingrese el ID del registro que desea \
                                        modificar', value=0, min_value=0,
                                       max_value=len(df)-1)
            actividad = st.text_input('Actividad')
            tipo = st.selectbox('Tipo', options=['Gasto', 'Ingreso'])
            monto = st.number_input('Monto', value=0.0)
            descripcion = st.text_input('Descripción')

            fecha = st.date_input('Fecha')
            hora = st.time_input('Hora')

            # Botón de envío del formulario
            submit_button = st.form_submit_button(label='Modificar')

            if submit_button:

                # Obtener el ID del usuario
                user_id = st.session_state.get('user_id')

                # Combinar fecha y hora
                fecha_hora = datetime.combine(fecha, hora)

                # Modificar el registro en la base de datos
                db.modificar_registro_financiero(
                    user_id, actividad, tipo, monto, descripcion, fecha_hora,
                    registro
                )

                # Mostrar un mensaje de éxito
                st.success("Registro modificado con éxito.")
                time.sleep(2)
                st.rerun()

    # Crear un expander para eliminar registros
    with st.expander("Eliminar un registro"):
        # Crear un formulario para eliminar registros
        with st.form(key='eliminar_form'):
            registro = st.number_input('Ingrese el ID del registro que desea \
                                        eliminar', value=0)

            # Botón de envío del formulario
            submit_button = st.form_submit_button(label='Eliminar')

            if submit_button:
                # Eliminar el registro de la base de datos
                db.eliminar_registro_financiero(user_id, registro)

                # Mostrar un mensaje de éxito
                st.success("Registro eliminado con éxito.")
                time.sleep(2)
                st.rerun()

# Si el usuario no tiene registros financieros, mostrar un mensaje
else:
    st.warning("No tienes registros financieros.")
    st.write("¡Agrega uno ahora!")
    st.stop()
