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
# - pytz: Para obtener la zona horaria de Colombia
# - numpy: Para realizar cálculos matemáticos
import time
from datetime import datetime
import pytz
import streamlit as st

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
if auth.login_with_cookie():
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


def validar_campos():
    """
    Valida que los campos no estén vacíos.

    Args:
        None

    Returns:
        None
    """

    if not actividad:
        st.warning("Por favor, ingresa una actividad.")
        return False

    if not monto:
        st.warning("Por favor, ingresa un monto.")
        return False

    if not fecha:
        st.warning("Por favor, selecciona una fecha.")
        return False

    if not st.session_state['hora']:
        st.warning("Por favor, selecciona una hora.")
        return False

    return True


def limpiar_campos():
    """
    Limpia los campos de entrada.

    Args:
        None

    Returns:
        None
    """
    del st.session_state.actividad
    del st.session_state.tipo
    del st.session_state.monto
    del st.session_state.descripcion


# Título de la página
st.title("Registrar actividad")


st.markdown(
    """
    En esta sección podrás registrar tus gastos e ingresos. Para ello, llena
    los campos solicitados y presiona el botón "Registrar actividad". Una vez
    que hayas registrado la actividad, se mostrará un mensaje de confirmación.
    """
)

# Hora y fecha actuales colombianas
timezone = pytz.timezone('America/Bogota')
fecha_hora_actual = datetime.now(timezone)

# Extraer la fecha y la hora
fecha = fecha_hora_actual.date()
hora = fecha_hora_actual.time()


# Inicializar las variables de estado de sesión si no existen
if "actividad" not in st.session_state:
    st.session_state.actividad = None
    st.session_state.tipo = None
    st.session_state.monto = None
    st.session_state.descripcion = None

# Si la hora no ha sido seleccionada, usar la hora actual
if 'hora' not in st.session_state or st.session_state['hora'] is None:
    st.session_state['hora'] = hora

tipo = st.selectbox("Tipo de actividad", ["Gasto", "Ingreso"],
                    placeholder="Selecciona una opción",
                    index=None, key="tipo")

actividad = st.text_input("Actividad", value=None, key="actividad",
                          placeholder="Ej: Compra de gasolina")

monto = st.number_input("Monto", value=None, min_value=0, step=1,
                        placeholder="Ej: 50000", key="monto")

if monto:
    st.markdown(f"**Valor:** ${monto:,.0f}")

# Crear un marcador de posición para el widget st.date_input
fecha_placeholder = st.empty()

# Ahora puedes usar fecha_formateada en tus widgets de Streamlit
fecha_formateada_ph = st.empty()

# Crear un marcador de posición para el widget st.time_input
hora_placeholder = st.empty()

descripcion = st.text_area("Descripción", value=None, key="descripcion",
                           placeholder="Ej: Compra de gasolina para la moto")

# Usar fecha y hora en los widgets de Streamlit
fecha = fecha_placeholder.date_input("Fecha", fecha, format="DD/MM/YYYY")
hora_usuario = hora_placeholder.time_input("Hora", st.session_state.hora,
                                           key="hora")

# Combinar la fecha y la hora en un solo objeto datetime
fecha_hora = datetime.combine(fecha, st.session_state.hora)

# Formatear la fecha
meses = [
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]

fecha_formateada = (
                    f"{fecha_hora.day} de {meses[fecha_hora.month - 1]} "
                    f"del {fecha_hora.year}"
)

fecha_formateada_ph.write(f"Fecha: {fecha_formateada}")

if hora_usuario != st.session_state.hora:
    del st.session_state.hora
    st.session_state.hora = hora_usuario

campos_validos = validar_campos()

if st.button("Registrar actividad") and campos_validos:

    user_id = st.session_state.get("user_id")

    # Insertar la actividad en la base de datos
    db.insertar_registro_financiero(actividad, tipo, monto,
                                    descripcion, fecha_hora, user_id)

    # Mostrar mensaje de confirmación
    st.success("Actividad registrada correctamente.")

    # Limpiar los campos
    limpiar_campos()

    # Actualizar la hora en la variable de estado de sesión
    del st.session_state.hora

    # Redirigir a la página de registro de actividad
    time.sleep(2)
    st.switch_page("pages/registro_actividad.py")
