from flask import Blueprint, render_template, request, redirect, url_for
from firebase_config import db

asignatura_bp = Blueprint('asignaturas', __name__)

# 📋 Listar asignaturas
@asignatura_bp.route('/asignaturas')
def listar_asignaturas():
    asignaturas_ref = db.collection("asignaturas").get()
    asignaturas = [doc.to_dict() for doc in asignaturas_ref]
    return render_template("asignaturas/listar.html", asignaturas=asignaturas)

# 📋 Crear asignatura
@asignatura_bp.route('/asignaturas/crear', methods=['GET', 'POST'])
def crear_asignatura():
    if request.method == 'POST':
        id_asignatura = request.form['id_asignatura']
        nombre = request.form['nombre']
        creditos = int(request.form['creditos'])
        estado = request.form['estado']

        db.collection("asignaturas").add({
            "id_asignatura": id_asignatura,
            "nombre": nombre,
            "creditos": creditos,
            "estado": estado
        })
        return redirect(url_for('asignaturas.listar_asignaturas'))

    return render_template("asignaturas/crear.html")
