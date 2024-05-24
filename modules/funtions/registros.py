import streamlit as st
import numpy as np
from ..db import ConexionDB

def calcular_estadisticas(resultados):
    """
    Calcula las estadísticas de gastos e ingresos.

    Args:
        resultados (list): Lista de tuplas con los resultados de la consulta a la base de datos.

    Returns:
        dict: Diccionario con las estadísticas calculadas.
    """
    # Convertir resultados en un array de NumPy
    resultados_np = np.array(resultados)

    # Crear máscaras booleanas para gastos e ingresos
    mascara_gastos = resultados_np[:, 0] == 'Gasto'
    mascara_ingresos = resultados_np[:, 0] == 'Ingreso'

    # Usar las máscaras booleanas para filtrar gastos e ingresos
    gastos = resultados_np[mascara_gastos, 1]
    ingresos = resultados_np[mascara_ingresos, 1]

    # Calcular estadísticas para gastos e ingresos
    estadisticas = {
        "gastos": {
            "promedio": np.mean(gastos) if len(gastos) > 0 else 0,
            "mediana": np.median(gastos) if len(gastos) > 0 else 0,
            "desviacion": np.std(gastos) if len(gastos) > 0 else 0
        },
        "ingresos": {
            "promedio": np.mean(ingresos) if len(ingresos) > 0 else 0,
            "mediana": np.median(ingresos) if len(ingresos) > 0 else 0,
            "desviacion": np.std(ingresos) if len(ingresos) > 0 else 0
        }
    }

    return estadisticas, gastos, ingresos

def visualizar_estadisticas():
    """
    Visualiza las estadísticas de gastos e ingresos de un usuario.

    Args:
        None

    Returns:
        None
    """

    # Crear una instancia de la conexión a la base de datos
    db = ConexionDB()
    conn = db.conectar()

    # Consultar los datos de gastos e ingresos de la base de datos
    query = """
    SELECT tipo, monto
    FROM registros_financieros
    WHERE user_id = %s
    """
    user_id = st.session_state.get('user_id')
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    resultados = cursor.fetchall()

    if resultados:

        st.write("## Estadísticas de Gastos e Ingresos")
        st.write("-------------------------------")

        # Convertir resultados en un array de NumPy
        resultados_np = np.array(resultados)

        # Crear máscaras booleanas para gastos e ingresos
        mascara_gastos = resultados_np[:, 0] == 'Gasto'
        mascara_ingresos = resultados_np[:, 0] == 'Ingreso'

        # Usar las máscaras booleanas para filtrar gastos e ingresos
        gastos = resultados_np[mascara_gastos, 1]
        ingresos = resultados_np[mascara_ingresos, 1]

        if len(gastos) > 0:
            # Calcular estadísticas para gastos
            promedio_gastos = np.mean(gastos)
            mediana_gastos = np.median(gastos)
            desviacion_gastos = np.std(gastos)
        else:
            promedio_gastos = mediana_gastos = desviacion_gastos = 0

        if len(ingresos) > 0:
            # Calcular estadísticas para ingresos
            promedio_ingresos = np.mean(ingresos)
            mediana_ingresos = np.median(ingresos)
            desviacion_ingresos = np.std(ingresos)
        else:
            promedio_ingresos = mediana_ingresos = desviacion_ingresos = 0

        # Mostrar estadísticas
        st.subheader("Estadísticas de Gastos")
        st.write(f"Promedio: {promedio_gastos:.2f}")
        st.write(f"Mediana: {mediana_gastos:.2f}")
        st.write(f"Desviación Estándar: {desviacion_gastos:.2f}")

        st.subheader("Estadísticas de Ingresos")
        st.write(f"Promedio: {promedio_ingresos:.2f}")
        st.write(f"Mediana: {mediana_ingresos:.2f}")
        st.write(f"Desviación Estándar: {desviacion_ingresos:.2f}")
    else:
        st.warning("No hay datos disponibles para mostrar las estadísticas.")

    # Cerrar la conexión a la base de datos
    db.cerrar()

    '''
        # Calcular estadísticas
        estats = calcular_estadisticas(resultados)

        # Mostrar las estadísticas de gastos e ingresos
        st.subheader("Estadísticas de Gastos")
        st.write(f"Promedio: {estats['gastos']['promedio']:.2f}")
        st.write(f"Mediana: {estats['gastos']['mediana']:.2f}")
        st.write(
            f"Desviación Estándar: {estats['gastos']['desviacion']:.2f}"
            )

        st.write("---")

        st.subheader("Estadísticas de Ingresos")
        st.write(f"Promedio: {estats['ingresos']['promedio']:.2f}")
        st.write(f"Mediana: {estats['ingresos']['mediana']:.2f}")
        st.write(
            f"Desviación Estándar: {estats['ingresos']['desviacion']:.2f}"
            )
    else:
        st.warning("No hay datos disponibles para mostrar las estadísticas.")

    # Cerrar la conexión a la base de datos
    db.cerrar()
    '''


# Visualizar las estadísticas de gastos e ingresos
visualizar_estadisticas()
