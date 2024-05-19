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
import time
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
time.sleep(2)

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

# Crear un marcador de posición para el widget st.time_input
hora_placeholder = st.empty()

# Si la hora no ha sido seleccionada, usar la hora actual
if 'hora' not in st.session_state:
    st.session_state['hora'] = fecha_hora_actual.time()

# Ahora puedes usar fecha y hora en tus widgets de Streamlit
fecha = st.date_input("Fecha", fecha, format="DD/MM/YYYY")
hora = hora_placeholder.time_input("Hora", st.session_state['hora'])

# Actualizar st.session_state['hora'] con la hora seleccionada
st.session_state['hora'] = hora

# Formatear la fecha
meses = [
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]

# Combinar la fecha y la hora en un solo objeto datetime
fecha_hora = datetime.combine(fecha, st.session_state['hora'])

fecha_formateada = (
                    f"{fecha_hora.day} de {meses[fecha_hora.month - 1]} "
                    f"del {fecha_hora.year}"
)

# Ahora puedes usar fecha_formateada en tus widgets de Streamlit
st.write(f"Fecha: {fecha_formateada}")

descripcion = st.text_area("Descripción")

if st.button("Registrar actividad"):

    user_id = st.session_state.get("user_id")
    # Combinar la fecha y la hora en un solo objeto datetime
    fecha_hora = datetime.combine(fecha, st.session_state['hora'])

    # Insertar la actividad en la base de datos
    db.insertar_registro_financiero(actividad, tipo, monto,
                                    descripcion, fecha_hora, user_id)

    # Mostrar mensaje de confirmación
    st.success("Actividad registrada correctamente.")

    # Reiniciar la variable de estado de sesión
    st.session_state['registrar_actividad_presionado'] = False
    st.session_state['hora'] = None

    # Reiniciar los campos del formulario
    st.switch_page("pages/registrar_actividad.py")

st.markdown(
    """
    En esta sección podrás registrar tus gastos e ingresos. Para ello, llena
    los campos solicitados y presiona el botón "Registrar actividad". Una vez
    que hayas registrado la actividad, se mostrará un mensaje de confirmación.
    """
)
