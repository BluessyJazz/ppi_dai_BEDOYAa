"""
Este script se encarga de visualizar las estadísticas de la actividad de los
usuarios. Se conecta a la base de datos para obtener los registros financieros
de un usuario y calcular las estadísticas de gastos e ingresos.
"""

# Importar librerías
# - time: Para pausar la ejecución del script
# - streamlit: Para la interfaz web
# - pandas: Para trabajar con DataFrames
# - datetime: Para obtener la fecha y hora actuales
import time
import pandas as pd
from datetime import datetime
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
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
    page_title="Análisis de Registros · Wily MotoTrack",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título de la página
st.title("Análisis de Registros")

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

if not resultados:
    st.warning("No hay registros financieros para analizar.")
    st.write("Por favor, agrega registros financieros para ver las \
             estadísticas.")
    st.stop()

else:
    # Crear un DataFrame con los registros financieros
    df = pd.DataFrame(resultados, columns=["ID", "Actividad", "Tipo", "Monto",
                                           "Descripción", "Fecha"])

    # Establecer el ID como índice
    df.set_index("ID", inplace=True)

    # Guardar el DataFrame en el estado de la sesión
    st.session_state.df = df

if 'df' in st.session_state and not st.session_state.df.empty:
    df = st.session_state.df

    # Calcular las estadísticas de gastos e ingresos con numpy
    gastos = df[df["Tipo"] == "Gasto"]["Monto"].sum()
    ingresos = df[df["Tipo"] == "Ingreso"]["Monto"].sum()
    balance = ingresos - gastos

    # Tres columnas para mostrar los resultados
    col1, col2, col3 = st.columns(3)

    # Mostrar los resultados
    col1.write("### Gastos 💸")
    col1.write(f"<span style='color:#ff7675'>${gastos:,.0f}</span>",
               unsafe_allow_html=True)

    col2.write("### Ingresos 💰")
    col2.write(f"<span style='color:#00b894'>${ingresos:,.0f}</span>",
               unsafe_allow_html=True)

    # Mostrar el balance en verde si es positivo y en rojo si es negativo
    if balance >= 0:
        col3.write("### Balance 💵")
        col3.write(f"<span style='color:#00b894'>${balance:,.0f}</span>",
                   unsafe_allow_html=True)
    else:
        col3.write("### Balance 💵")
        col3.write(f"<span style='color:#ff7675'>-${-balance:,.0f}</span>",
                   unsafe_allow_html=True)

    # Convertir 'Fecha' a datetime y extraer solo la parte de la fecha
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Monto'] = df['Monto'].astype(float)

    # Dataframe con conteo y monto por tipo
    df_tipo = df.groupby('Tipo').agg({'Monto': ['count', 'sum']})
    df_tipo.columns = ['Cantidad', 'Total']

    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Calcular la fecha hace un mes
    fecha_mes_anterior = fecha_actual - pd.DateOffset(months=1)

    # Filtrar df por el último mes
    df_ultimo_mes = df[(df['Fecha'] >= fecha_mes_anterior) & (df['Fecha'] < fecha_actual)]

    # Crear df_tipo_mes agrupando por 'Tipo' y calculando el conteo
    # y la suma de 'Monto'
    df_tipo_mes = df_ultimo_mes.groupby('Tipo').agg({'Monto': ['count', 'sum']})
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
    df_actividad_ingreso = df[df["Tipo"] == "Ingreso"].groupby('Actividad').agg({'Monto': ['count', 'sum']})
    df_actividad_ingreso.columns = ['Cantidad', 'Total']
    df_actividad_ingreso = df_actividad_ingreso.sort_values(by='Total', ascending=False)

    df_actividad_gasto = df[df["Tipo"] == "Gasto"].groupby('Actividad').agg({'Monto': ['count', 'sum']})
    df_actividad_gasto.columns = ['Cantidad', 'Total']
    df_actividad_gasto = df_actividad_gasto.sort_values(by='Total', ascending=False)

    st.header("Resumen de Actividades")

    col1, col2 = st.columns(2)

    col1.write("### Ingresos 💰")
    col1.write(df_actividad_ingreso)

    col2.write("### Gastos 💸")
    col2.write(df_actividad_gasto)

    # Calcular el número total de días en el rango de fechas
    total_dias = (df["Fecha"].max() - df["Fecha"].min()).days

    # Calcular el gasto promedio diario
    gasto_promedio_diario = gastos / total_dias

    # Calcular el ingreso promedio diario
    ingreso_promedio_diario = ingresos / total_dias

    # Dos columnas para mostrar los resultados
    col1, col2 = st.columns(2)

    # Mostrar los resultados
    col1.write("### Gasto Promedio Diario")
    col1.write(f"${gasto_promedio_diario:,.0f}")

    col2.write("### Ingreso Promedio Diario")
    col2.write(f"${ingreso_promedio_diario:,.0f}")

    # df_gastos y df_ingresos
    df_gastos = df[df['Tipo'] == 'Gasto']
    df_ingresos = df[df['Tipo'] == 'Ingreso']

    # Gastos e ingresos agrupados por mes
    df_gastos_mes = df_gastos.groupby(
                        df_gastos['Fecha'].dt.to_period('M'))['Monto'].sum()
    df_ingresos_mes = df_ingresos.groupby(
                        df_ingresos['Fecha'].dt.to_period('M'))['Monto'].sum()

    # Convertir los números de los meses a nombres de meses
    df_gastos_mes.index = df_gastos_mes.index.strftime('%B')
    df_ingresos_mes.index = df_ingresos_mes.index.strftime('%B')

    # Dos columnas para gráfico de barras de gastos e ingresos
    col1, col2 = st.columns(2)

    # Mostrar los resultados
    with col1:
        st.header("Gastos por Mes")
        df_gastos_mes.plot(kind='bar', color='purple')
        plt.title('Gastos por Mes')
        plt.xlabel('Mes')
        plt.ylabel('Monto')
        st.pyplot(plt)
        plt.clf()

    with col2:
        st.header("Ingresos por Mes")
        df_ingresos_mes.plot(kind='bar', color='purple')
        plt.title('Ingresos por Mes')
        plt.xlabel('Mes')
        plt.ylabel('Monto')
        st.pyplot(plt)
        plt.clf()

    # Agrupar los gastos e ingresos por 'Actividad' y sumar los 'Montos'
    gastos_actividad = df_gastos.groupby('Actividad')['Monto'].sum()
    ingresos_actividad = df_ingresos.groupby('Actividad')['Monto'].sum()

    # Dos columnas para gráfico de dona de gastos e ingresos según 'Actividad'
    col1, col2 = st.columns(2)

    # Mostrar los resultados
    with col1:
        # Gráfico de dona para los gastos
        plt.pie(gastos_actividad, labels=gastos_actividad.index, startangle=90, autopct='%1.1f%%')
        plt.gca().add_artist(plt.Circle((0,0),0.70,fc='white'))
        plt.title('Gastos por Actividad')
        st.pyplot(plt)
        plt.clf()

    with col2:
        # Gráfico de dona para los ingresos
        plt.pie(ingresos_actividad, labels=ingresos_actividad.index, startangle=90, autopct='%1.1f%%')
        plt.gca().add_artist(plt.Circle((0,0),0.70,fc='white'))
        plt.title('Ingresos por Actividad')
        st.pyplot(plt)
        plt.clf()


    # Extraer los pares únicos de mes-año
    meses = df['Fecha'].dt.to_period('M').unique().strftime('%B - %Y')

    # Titulo para filtrar por mes
    st.header("Análisis Mensual")

    # Widget de selección de mes
    mes_seleccionado = st.selectbox('Seleccione un mes', meses)

    # Convertir la selección del usuario a un objeto datetime
    mes_seleccionado = datetime.strptime(mes_seleccionado, '%B - %Y')

    # Filtrar el DataFrame para el mes seleccionado
    df_mes = df[(df['Fecha'].dt.year == mes_seleccionado.year) & (df['Fecha'].dt.month == mes_seleccionado.month)]

    # Filtrar el DataFrame para los gastos e ingresos del mes seleccionado
    df_gastos = df_mes[df_mes['Tipo'] == 'Gasto']
    df_ingresos = df_mes[df_mes['Tipo'] == 'Ingreso']

    # Agrupar los gastos e ingresos por día y sumar los montos
    df_gastos = df_gastos.groupby(df_gastos['Fecha'].dt.day)['Monto'].sum()
    df_ingresos = df_ingresos.groupby(
                                df_ingresos['Fecha'].dt.day)['Monto'].sum()

    # Dos columnas para gasto e ingreso promedio diarios del mes seleccionado
    col1, col2 = st.columns(2)

    # Mostrar los resultados
    with col1:
        # Verificar si hay suficientes datos para calcular el gasto promedio
        if df_gastos.empty:
            st.write("### Gasto Promedio")
            st.warning("No hay suficientes datos para calcular el gasto promedio.")
        else:
            # Calcular el gasto promedio diario del mes seleccionado
            gasto_promedio_diario_mes = df_gastos.mean()
            st.write("### Gasto Promedio")
            st.write(f"${gasto_promedio_diario_mes:,.0f}")

    with col2:
        # Verificar si hay suficientes datos para calcular el ingreso promedio
        if df_ingresos.empty:
            st.write("### Ingreso Promedio")
            st.warning("No hay suficientes datos para calcular el ingreso promedio.")
        else:
            # Calcular el ingreso promedio diario del mes seleccionado
            ingreso_promedio_diario_mes = df_ingresos.mean()
            st.write("### Ingreso Promedio")
            st.write(f"${ingreso_promedio_diario_mes:,.0f}")

    # Dos columnas
    col1, col2 = st.columns(2)

    # Mostrar los resultados
    with col1:
        # Verificar si hay suficientes datos para mostrar el gráfico
        if df_gastos.empty:
            st.warning("No hay suficientes datos para mostrar el gráfico de gastos.")
        else:
            # Crear un gráfico de barras de los gastos por día
            df_gastos.plot(kind='bar', color='purple')
            plt.title('Gastos por día')
            plt.xlabel('Día')
            plt.ylabel('Monto')
            st.pyplot(plt)
            plt.clf()

    with col2:
        # Verificar si hay suficientes datos para mostrar el gráfico
        if df_ingresos.empty:
            st.warning("No hay suficientes datos para mostrar el gráfico de ingresos.")
        else:
            # Crear un gráfico de barras de los ingresos por día
            df_ingresos.plot(kind='bar', color='purple')
            plt.title('Ingresos por día')
            plt.xlabel('Día')
            plt.ylabel('Monto')
            st.pyplot(plt)
            plt.clf()
