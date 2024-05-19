import streamlit as st
import numpy as np
from ..db import ConexionDB


def visualizar_estadisticas():
    """
    Visualiza las estadísticas de gastos e ingresos de un usuario.

    Args:
        None

    Returns:
        None
    """
    st.title("Estadísticas de Gastos e Ingresos")

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

        st.write("Estadísticas de Gastos e Ingresos")
        st.write("-------------------------------")
        st.write(resultados)

        # Convertir resultados en un array de NumPy
        resultados_np = np.array(resultados)

        st.write("---")
        st.write("resultados_np")
        st.write(resultados_np)

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
