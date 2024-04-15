import mysql.connector
import streamlit as st
import pandas as pd

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="daker2002",
    database="wilymoto"
)

print("conectada")
