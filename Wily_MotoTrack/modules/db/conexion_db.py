"""
Módulo para la conexión a la base de datos MySQL en una aplicación de Streamlit.

Este módulo proporciona funciones para conectarse a una base de datos
MySQL y realizar consultas.

Usage:
    from modules.db.connection import conectar_db, consultar_datos

    # Establecer conexión a la base de datos
    conexion = conectar_db()

    # Realizar una consulta a la base de datos
    consulta = "SELECT * FROM nombre_de_la_tabla;"
    resultados = consultar_datos(consulta)

    # Procesar los resultados
    if resultados:
        for resultado in resultados:
            print(resultado)
    else:
        print("No se pudieron obtener los datos de la base de datos.")
"""

