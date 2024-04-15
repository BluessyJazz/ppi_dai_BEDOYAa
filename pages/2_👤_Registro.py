"""
Este módulo contiene la implementación de la página de registro de usuarios

"""

import sys
sys.path.append('./modules')  # Replace '/path/to/modules' with the actual path
                                #to the 'modules' directory

import streamlit as st
from modules.db.conexion_db import insertar_usuario

st.set_page_config(page_title="Iniciar Sesión", page_icon="👤")

st.markdown("# Registro de Usuarios")



nombre = st.text_input("Nombre")
correo = st.text_input("Correo Electrónico")
contrasena = st.text_input("Contraseña", type="password")

if st.button("Registrarse"):
    if nombre and correo and contrasena:
        # Insertar usuario en la base de datos
        insertar_usuario(nombre, correo, contrasena)
        st.success("¡Registro exitoso! Por favor inicia sesión.")
    else:
        st.error("Por favor completa todos los campos.")







'''# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from usuarios;', ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"{row.nombre} has a :{row.correo}:y :{row.contrasena}:")




cursor = conectar_db().cursor()
cursor.execute("SELECT * FROM usuarios")
resultados = cursor.fetchall()'''