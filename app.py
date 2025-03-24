from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from models.user import Usuario
from conexion.conexion import obtener_conexion
import bcrypt

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_email(user_id)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = bcrypt.hashpw(request.form["password"].encode("utf-8"), bcrypt.gensalt())

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", (nombre, email, password))
        conexion.commit()
        cursor.close()
        conexion.close()
        flash("Usuario registrado con éxito", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"].encode("utf-8")

        usuario = Usuario.obtener_por_email(email)
        if usuario and bcrypt.checkpw(password, usuario.password.encode("utf-8")):
            login_user(usuario)
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Credenciales incorrectas", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    flash("Sesión cerrada", "info")
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
