from flask_login import UserMixin
from conexion.conexion import obtener_conexion

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    @staticmethod
    def obtener_por_email(email):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conexion.close()
        if user:
            return Usuario(user["id_usuario"], user["nombre"], user["email"], user["password"])
        return None
