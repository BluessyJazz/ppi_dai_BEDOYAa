"""
Esta página es la encargada de registrar los gastos e ingresos de los
usuarios. Para ello, se muestran los campos necesarios para ingresar la
información y se almacena en la base de datos. Además, se muestra un
mensaje de confirmación al usuario una vez que se ha registrado la
actividad correctamente.
"""

# Importar librerías
# - streamlit: Para la interfaz web
# - datetime: Para obtener la fecha y hora actuales
# - numpy: Para realizar cálculos matemáticos
import streamlit as st
from datetime import datetime

# Importar módulos locales
# - init_auth: Para inicializar la autenticación
# - menu: Para mostrar el menú de la aplicación en la barra lateral
from modules.db import ConexionDB
from modules.auth import init_auth
from menu import menu

# Configuración de la página
st.set_page_config(
    page_title="Registrar actividad · Wily MotoTrack",
    page_icon="🏍️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Inicializar la autenticación
auth = init_auth()

# Autenticar al usuario
auth.silence_login()

# Si el usuario no está autenticado, mostrar el menú sin autenticación
if (
    'authentication_status' not in st.session_state or
    not st.session_state['authentication_status']
):
    menu(auth=None)
    st.switch_page("main.py")

# Si el usuario está autenticado, mostrar el menú
else:
    menu(auth)

# Crear una instancia de la conexión a la base de datos
db = ConexionDB()

from modules.funtions.registros import visualizar_estadisticas

visualizar_estadisticas()

# Título de la página
st.title("Registrar actividad")

st.session_state

tipo = st.selectbox("Tipo de actividad", ["Gasto", "Ingreso"])

actividad = st.text_input("Actividad")

monto = st.number_input("Monto", min_value=0, step=1)

import pytz

# Hora y fecha actuales colombianas
timezone = pytz.timezone('America/Bogota')
fecha_hora_actual = datetime.now(timezone)

# Extraer la fecha y la hora
fecha = fecha_hora_actual.date()
hora = fecha_hora_actual.time()

# Ahora puedes usar fecha y hora en tus widgets de Streamlit
fecha = st.date_input("Fecha", fecha)
hora = st.time_input("Hora", hora)

# Combinar la fecha y la hora en un solo objeto datetime
fecha_hora = datetime.combine(fecha, hora)

descripcion = st.text_area("Descripción")

if st.button("Registrar actividad"):
    # Mostrar mensaje de verificación
    st.write("Registro a guardar:")
    st.write(f"Tipo de actividad: {tipo}")
    st.write(f"Actividad: {actividad}")
    st.write(f"Monto: {monto}")
    st.write(f"Fecha: {fecha}")

    # Establecer una variable de estado de sesión para rastrear si el botón
    # "Registrar actividad" ha sido presionado
    st.session_state['registrar_actividad_presionado'] = True

# Si el botón "Registrar actividad" ha sido presionado, mostrar el botón
# "Confirmar"
if st.session_state.get('registrar_actividad_presionado', False):
    if st.button("Confirmar"):

        user_id = st.session_state.get("user_id")

        # Insertar la actividad en la base de datos
        db.insertar_registro_financiero(actividad, tipo, monto,
                                        descripcion, fecha, user_id)

        # Mostrar mensaje de confirmación
        st.success("Actividad registrada correctamente.")

        # Reiniciar la variable de estado de sesión
        st.session_state['registrar_actividad_presionado'] = False

        # Reiniciar los campos del formulario
        st.rerun()

st.markdown(
    """
    En esta sección podrás registrar tus gastos e ingresos. Para ello, llena
    los campos solicitados y presiona el botón "Registrar actividad". Una vez
    que hayas registrado la actividad, se mostrará un mensaje de confirmación.
    """
)
