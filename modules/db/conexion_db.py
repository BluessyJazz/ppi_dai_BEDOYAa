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

import streamlit as st

# Inicializar la conexión a la base de datos


def insertar_usuario(nombre, correo_electronico, contrasena):
    conn = st.connection('mysql', type='sql')

    # Añadir usuario
    conn.query(
        """
        INSERT INTO usuarios (nombre, correo_electronico, contrasena)
        VALUES ('{}', '{}', '{}')
        """.format(nombre, correo_electronico, contrasena)
    )

    conn.commit()

'''import mysql.connector

def conectar_db():
    """
    Establece una conexión a la base de datos MySQL.

    Returns:
        mysql.connector.connection.MySQLConnection: Objeto de conexión a la base de datos.
    """
    try:
        # Establecer la conexión a la base de datos
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="usuarios"
        )
        return conexion
    except mysql.connector.Error as error:
        print(f"Error al conectar a la base de datos: {error}")
        return None
'''
