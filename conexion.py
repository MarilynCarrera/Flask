import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tu_contraseña",
        database="desarrollo_web"
    )
