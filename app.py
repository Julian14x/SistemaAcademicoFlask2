from flask import Flask
from flask import Blueprint, render_template, request, redirect, session

# IMPORTAR BLUEPRINTS
from routes.estudiantes import estudiante_bp
from routes.matricula import matricula_bp
from routes.alerta import alerta_bp
from routes.auth_routes import auth_bp
from routes.dashboard import dashboard_bp
from routes.home import home_bp
from routes.asignaturas import asignatura_bp
# Crear aplicación en Flask
app = Flask(__name__)

# CLAVE SECRETA (para sesiones y seguridad)
app.secret_key = 'clave_secreta'



# REGISTRAR BLUEPRINTS
app.register_blueprint(estudiante_bp)
app.register_blueprint(matricula_bp)
app.register_blueprint(alerta_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(home_bp)
app.register_blueprint(asignatura_bp)

app.secret_key = "clave-secreta"


# Ruta principal
@app.route('/')
def home():
    return render_template('home.html')

# Ruta dashboard (redirige después del login)
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# EJECUTAR APLICACIÓN
if __name__ == '__main__':
    app.run(debug=True)
