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

st.write(resultados)

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

    # Mostrar las estadísticas
    st.write("### Estadísticas")
    st.write(f"**Gastos:** ${gastos:.2f}")
    st.write(f"**Ingresos:** ${ingresos:.2f}")
    st.write(f"**Balance:** ${balance:.2f}")

    # Analisis exahustivo de los registros
    st.write("### Análisis de Registros")
    st.write("#### Actividad")
    st.write(df["Actividad"].value_counts())
    st.write("#### Tipo")
    st.write(df["Tipo"].value_counts())
    st.write("#### Monto")
    st.write(df["Monto"].describe())
    st.write("#### Fecha")
    st.write(df["Fecha"].describe())
    
    # Calcular gasto promedio diario
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df["Día"] = df["Fecha"].dt.day_name()
    df["Mes"] = df["Fecha"].dt.month_name()
    df["Año"] = df["Fecha"].dt.year
    gasto_promedio_diario = df[df["Tipo"] == "Gasto"].groupby("Día")["Monto"].mean()
    st.write("#### Gasto Promedio Diario")
    st.write(gasto_promedio_diario)

    # Calcular gasto promedio mensual
    gasto_promedio_mensual = df[df["Tipo"] == "Gasto"].groupby("Mes")["Monto"].mean()
    st.write("#### Gasto Promedio Mensual")
    st.write(gasto_promedio_mensual)

    # Calcular gasto promedio anual
    gasto_promedio_anual = df[df["Tipo"] == "Gasto"].groupby("Año")["Monto"].mean()
    st.write("#### Gasto Promedio Anual")
    st.write(gasto_promedio_anual)

    # Calcular gasto total por mes
    gasto_total_mes = df[df["Tipo"] == "Gasto"].groupby("Mes")["Monto"].sum()
    st.write("#### Gasto Total por Mes")
    st.write(gasto_total_mes)
    
    # Calcular gasto total por año
    gasto_total_anual = df[df["Tipo"] == "Gasto"].groupby("Año")["Monto"].sum()
    st.write("#### Gasto Total por Año")
    st.write(gasto_total_anual)

    


