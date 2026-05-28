from flask import Blueprint, render_template, request, redirect, session
from firebase_admin import firestore
from firebase_config import db


auth_bp = Blueprint('auth', __name__)
db = firestore.client()

# LOGIN
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Buscar usuario en Firestore
        usuarios_ref = db.collection("usuarios") \
                         .where("username", "==", username) \
                         .where("password", "==", password) \
                         .get()

        if usuarios_ref:
            usuario = usuarios_ref[0].to_dict()
            session['usuario'] = usuario['username']
            session['rol'] = usuario['rol']
            return redirect('/dashboard')
        else:
            return render_template('auth/login.html', error="Usuario o contraseña incorrectos")

    return render_template('asignaturas/auth/login.html')

# LOGOUT
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# DECORADOR DE ROLES
def requiere_roles(roles_permitidos):
    def wrapper(func):
        def inner(*args, **kwargs):
            if 'rol' not in session or session['rol'] not in roles_permitidos:
                return redirect('/login')
            return func(*args, **kwargs)
        inner.__name__ = func.__name__
        return inner
    return wrapper
