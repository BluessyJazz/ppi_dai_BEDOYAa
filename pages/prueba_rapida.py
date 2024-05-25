"""
Este módulo contiene una prueba rápida para el usuario que no tiene una cuenta
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
import pandas as pd

# Importar módulos
from modules.auth import init_auth
from menu import menu


st.set_page_config(
    page_title="Prueba la app · Wily MotoTrack",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Inicializar la autenticación
auth = init_auth()

auth.login_with_cookie()

if (
    'authentication_status' not in st.session_state or
    not st.session_state['authentication_status']
):
    menu(auth=None)

else:
    st.write("Ya iniciaste sesión")
    menu(auth)
    st.stop()

st.title("Prueba rápida")
st.write("¡Bienvenido a la prueba rápida de Wily MotoTrack! 🚀")
st.write("Aquí podrás probar la aplicación sin necesidad de registrarte. \
          Al reiniciar la página se perderán los datos ingresados. \
          Para guardar tus datos, y ver gráficos detallados \
          regístrate en la aplicación.")

# Pestañas de la página
tab1, tab2, tab3 = st.tabs(
                ["Registrar actividad", "Ver actividades", "Ver análisis"])

with tab1:

    # Inicializar las variables de estado de sesión si no existen
    if "actividad" not in st.session_state:
        st.session_state.actividad = None
        st.session_state.tipo = None
        st.session_state.monto = None
        st.session_state.descripcion = None

    if "financial_records" not in st.session_state:
        st.session_state.financial_records = pd.DataFrame(columns=[
            "actividad", "tipo", "monto", "descripcion",
            "fecha_hora", "user_id"
        ])

    # Validar campos
    def validar_campos():
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

    # Limpiar campos
    def limpiar_campos():
        del st.session_state.actividad
        del st.session_state.tipo
        del st.session_state.monto
        del st.session_state.descripcion

    # Título de la página
    st.title("Registrar actividad")

    st.markdown("""
        En esta sección podrás registrar tus gastos e ingresos. Para ello, llena
        los campos solicitados y presiona el botón "Registrar actividad". Una vez
        que hayas registrado la actividad, se mostrará un mensaje de confirmación.
    """)

    # Hora y fecha actuales colombianas
    timezone = pytz.timezone('America/Bogota')
    fecha_hora_actual = datetime.now(timezone)

    # Extraer la fecha y la hora
    fecha = fecha_hora_actual.date()
    hora = fecha_hora_actual.time()

    # Si la hora no ha sido seleccionada, usar la hora actual
    if 'hora' not in st.session_state or st.session_state['hora'] is None:
        st.session_state['hora'] = hora

    # Campos del formulario
    tipo = st.selectbox("Tipo de actividad", ["Gasto", "Ingreso"],
                        placeholder="Selecciona una opción",
                        index=None, key="tipo")

    actividad = st.text_input("Actividad", value=None, key="actividad",
                              placeholder="Ej: Compra de gasolina")

    monto = st.number_input("Monto", value=None, min_value=0, step=1,
                            placeholder="Ej: 50000", key="monto")

    if monto:
        st.markdown(f"**Valor:** ${monto:,.0f}")

    descripcion = st.text_area(
                        "Descripción", value=None, key="descripcion",
                        placeholder="Ej: Compra de gasolina para la moto")

    # Usar fecha y hora en los widgets de Streamlit
    fecha = st.date_input("Fecha", fecha, format="DD/MM/YYYY")
    hora_usuario = st.time_input("Hora", st.session_state.hora, key="hora")

    # Combinar la fecha y la hora en un solo objeto datetime
    fecha_hora = datetime.combine(fecha, st.session_state.hora)

    # Formatear la fecha
    meses = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]

    fecha_formateada = (
        f"{fecha_hora.day} de {meses[fecha_hora.month - 1]} del {fecha_hora.year}"
    )

    st.write(f"Fecha: {fecha_formateada}")

    if hora_usuario != st.session_state.hora:
        del st.session_state.hora
        st.session_state.hora = hora_usuario

    # Validar los campos del formulario
    campos_validos = validar_campos()

    if st.button("Registrar actividad") and campos_validos:
        user_id = st.session_state.get("user_id", "test_user")  # Usar un ID de usuario de prueba
        nuevo_registro = {
            "actividad": actividad,
            "tipo": tipo,
            "monto": monto,
            "descripcion": descripcion,
            "fecha_hora": fecha_hora,
            "user_id": user_id
        }

        # Añadir el nuevo registro al DataFrame en el estado de sesión
        nuevo_registro_df = pd.DataFrame([nuevo_registro])
        st.session_state.financial_records = pd.concat([st.session_state.financial_records, nuevo_registro_df], ignore_index=True)

        # Mostrar mensaje de confirmación
        st.success("Actividad registrada correctamente.")

        # Limpiar los campos del formulario
        limpiar_campos()

        # Actualizar la hora en la variable de estado de sesión
        del st.session_state.hora

with tab2:
    st.title("Ver actividades")

    st.markdown("""
        En esta sección podrás ver todas las actividades que has registrado. Para ello,
        presiona el botón "Ver actividades" y se mostrará una tabla con los registros.
    """)

        # Asegurar que el DataFrame está en el estado de la sesión
    if "financial_records" not in st.session_state:
        st.session_state.financial_records = pd.DataFrame(columns=[
            "actividad", "tipo", "monto", "descripcion", "fecha_hora", "user_id"
        ])

    # Verificar si hay registros financieros
    if not st.session_state.financial_records.empty:
        df = st.session_state.financial_records.copy()
        df.reset_index(drop=True, inplace=True)
        df.index += 1  # Ajustar el índice para que comience desde 1
        df.index.name = "ID"

        # Opción de selección para ordenar el DataFrame
        orden = st.selectbox('Ordenar por', options=['ID', 'Fecha'])

        if orden == 'ID':
            df.sort_index(inplace=True)
        elif orden == 'Fecha':
            df.sort_values(by='fecha_hora', inplace=True)

        # Mostrar los registros financieros
        st.subheader("Registros Financieros")
        st.write(df)

        # Crear un expander para modificar registros
        with st.expander("Modificar un registro"):
            # Crear un formulario para modificar registros
            with st.form(key='modificar_form'):
                registro = st.number_input('Ingrese el ID del registro que desea modificar', value=1, min_value=1, max_value=len(df))
                actividad = st.text_input('Actividad', value=df.loc[registro, 'actividad'])
                tipo = st.selectbox('Tipo', options=['Gasto', 'Ingreso'], index=0 if df.loc[registro, 'tipo'] == 'Gasto' else 1)
                monto = st.number_input('Monto', value=df.loc[registro, 'monto'])
                descripcion = st.text_input('Descripción', value=df.loc[registro, 'descripcion'])

                fecha_hora = df.loc[registro, 'fecha_hora']
                fecha = st.date_input('Fecha', value=fecha_hora.date())
                hora = st.time_input('Hora', value=fecha_hora.time())

                # Botón de envío del formulario
                submit_button = st.form_submit_button(label='Modificar')

                if submit_button:
                    # Combinar fecha y hora
                    fecha_hora = datetime.combine(fecha, hora)

                    # Modificar el registro en el DataFrame
                    st.session_state.financial_records.at[registro - 1, 'actividad'] = actividad
                    st.session_state.financial_records.at[registro - 1, 'tipo'] = tipo
                    st.session_state.financial_records.at[registro - 1, 'monto'] = monto
                    st.session_state.financial_records.at[registro - 1, 'descripcion'] = descripcion
                    st.session_state.financial_records.at[registro - 1, 'fecha_hora'] = fecha_hora

                    # Mostrar un mensaje de éxito
                    st.success("Registro modificado con éxito.")
                    time.sleep(2)
                    st.experimental_rerun()

        # Crear un expander para eliminar registros
        with st.expander("Eliminar un registro"):
            # Crear un formulario para eliminar registros
            with st.form(key='eliminar_form'):
                registro = st.number_input('Ingrese el ID del registro que desea eliminar', value=1, min_value=1, max_value=len(df))

                # Botón de envío del formulario
                submit_button = st.form_submit_button(label='Eliminar')

                if submit_button:
                    # Eliminar el registro del DataFrame
                    st.session_state.financial_records.drop(index=registro - 1, inplace=True)
                    st.session_state.financial_records.reset_index(drop=True, inplace=True)

                    # Mostrar un mensaje de éxito
                    st.success("Registro eliminado con éxito.")
                    time.sleep(2)
                    st.experimental_rerun()

    # Si el usuario no tiene registros financieros, mostrar un mensaje
    else:
        st.warning("No tienes registros financieros.")
        st.write("¡Agrega uno ahora!")
        st.stop()

with tab3:
    # Asegurar que el DataFrame está en el estado de la sesión
    if "financial_records" not in st.session_state:
        st.session_state.financial_records = pd.DataFrame(columns=[
            "actividad", "tipo", "monto", "descripcion", "fecha_hora", "user_id"
        ])

    # Verificar si hay registros financieros
    if not st.session_state.financial_records.empty:
        df = st.session_state.financial_records.copy()
        df.reset_index(drop=True, inplace=True)
        df.index += 1  # Ajustar el índice para que comience desde 1
        df.index.name = "ID"

        # Calcular las estadísticas de gastos e ingresos con numpy
        gastos = df[df["tipo"] == "Gasto"]["monto"].sum()
        ingresos = df[df["tipo"] == "Ingreso"]["monto"].sum()
        balance = ingresos - gastos

        # Tres columnas para mostrar los resultados
        col1, col2, col3 = st.columns(3)

        # Mostrar los resultados
        col1.write("### Gastos 💸")
        col1.write(f"<span style='color:#ff7675'>${gastos:,.0f}</span>", unsafe_allow_html=True)

        col2.write("### Ingresos 💰")
        col2.write(f"<span style='color:#00b894'>${ingresos:,.0f}</span>", unsafe_allow_html=True)

        # Mostrar el balance en verde si es positivo y en rojo si es negativo
        if balance >= 0:
            col3.write("### Balance 💵")
            col3.write(f"<span style='color:#00b894'>${balance:,.0f}</span>", unsafe_allow_html=True)
        else:
            col3.write("### Balance 💵")
            col3.write(f"<span style='color:#ff7675'>-${-balance:,.0f}</span>", unsafe_allow_html=True)

        # Convertir 'fecha_hora' a datetime y extraer solo la parte de la fecha
        df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
        df['monto'] = df['monto'].astype(float)

        # Dataframe con conteo y monto por tipo
        df_tipo = df.groupby('tipo').agg({'monto': ['count', 'sum']})
        df_tipo.columns = ['Cantidad', 'Total']

        # Obtener la fecha actual
        fecha_actual = datetime.now()

        # Calcular la fecha hace un mes
        fecha_mes_anterior = fecha_actual - pd.DateOffset(months=1)

        # Filtrar df por el último mes
        df_ultimo_mes = df[(df['fecha_hora'] >= fecha_mes_anterior) & (df['fecha_hora'] < fecha_actual)]

        # Crear df_tipo_mes agrupando por 'tipo' y calculando el conteo y la suma de 'monto'
        df_tipo_mes = df_ultimo_mes.groupby('tipo').agg({'monto': ['count', 'sum']})
        df_tipo_mes.columns = ['Cantidad', 'Total']

        st.header("Resumen de Tipos de Registros")

        # Dos columnas para mostrar los resultados
        col1, col2 = st.columns(2)

        # Mostrar los resultados
        col1.write("### Totales 🌐")
        col1.write(df_tipo)

        col2.write("### Último mes 📅")
        col2.write(df_tipo_mes)

        # Dataframe con conteo y monto por actividad
        df_actividad_ingreso = df[df["tipo"] == "Ingreso"].groupby('actividad').agg({'monto': ['count', 'sum']})
        df_actividad_ingreso.columns = ['Cantidad', 'Total']
        df_actividad_ingreso = df_actividad_ingreso.sort_values(by='Total', ascending=False)

        df_actividad_gasto = df[df["tipo"] == "Gasto"].groupby('actividad').agg({'monto': ['count', 'sum']})
        df_actividad_gasto.columns = ['Cantidad', 'Total']
        df_actividad_gasto = df_actividad_gasto.sort_values(by='Total', ascending=False)

        st.header("Resumen de Actividades")

        col1, col2 = st.columns(2)

        col1.write("### Ingresos 💰")
        col1.write(df_actividad_ingreso)

        col2.write("### Gastos 💸")
        col2.write(df_actividad_gasto)

        # Calcular el número total de días en el rango de fechas
        total_dias = (df["fecha_hora"].max() - df["fecha_hora"].min()).days

        # Calcular el gasto promedio diario
        if total_dias != 0:
            gasto_promedio_diario = gastos / total_dias
            ingreso_promedio_diario = ingresos / total_dias
        else:
            gasto_promedio_diario = 0
            ingreso_promedio_diario = 0

        # Dos columnas para mostrar los resultados
        col1, col2 = st.columns(2)

        # Mostrar los resultados
        col1.write("### Gasto Promedio Diario")
        col1.write(f"${gasto_promedio_diario:,.0f}")

        col2.write("### Ingreso Promedio Diario")
        col2.write(f"${ingreso_promedio_diario:,.0f}")

    else:
        st.warning("No hay registros financieros para analizar.")
        st.write("Por favor, agrega registros financieros para ver las estadísticas.")
        st.stop()
