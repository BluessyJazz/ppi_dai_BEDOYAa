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
    layout="centered",
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

    # Gráficos
    st.header('Gráficos')
    df['Monto'] = df['Monto'].astype(int)
    df['Fecha'] = df['Fecha'].dt.to_pydatetime()
    df.groupby(df['Fecha'].dt.date)['Monto'].sum().plot(kind='bar')
    plt.title('Gastos e Ingresos por Fecha')
    plt.xlabel('Fecha')
    plt.ylabel('Monto')

    # Mostrar el gráfico
    st.pyplot(plt)

    # Estadísticas
    st.header('Análisis Estadístico')
    gastos = df[df['Tipo'] == 'Gasto']['Monto'].values
    ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].values
    media_gastos = np.mean(gastos)
    media_ingresos = np.mean(ingresos)
    t_stat, p_value = stats.ttest_ind(gastos, ingresos)
    st.write(f"Media de Gastos: {media_gastos}")
    st.write(f"Media de Ingresos: {media_ingresos}")
    st.write(f"T-Statistic: {t_stat}")
    st.write(f"P-Value: {p_value}")

    # Interpretación
    st.header('Interpretación de Resultados')
    if p_value < 0.05:
        if t_stat > 0:
            st.write("Los ingresos son significativamente mayores que los gastos. Esto es una buena señal de que tus ingresos superan a tus gastos.")
        else:
            st.write("Los gastos son significativamente mayores que los ingresos. Deberías revisar tus gastos y buscar maneras de reducirlos.")
    else:
        st.write("No hay una diferencia significativa entre los ingresos y los gastos. Tus ingresos y gastos están equilibrados.")

