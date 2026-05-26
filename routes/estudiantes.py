from flask import Blueprint, render_template, request, redirect
from firebase_admin import firestore
from routes.auth_routes import requiere_roles
from firebase_config import db


# Blueprint de estudiantes
estudiante_bp = Blueprint('estudiantes', __name__)
db = firestore.client()

# READ -> LISTAR ESTUDIANTES
@estudiante_bp.route('/estudiantes')
def listar_estudiantes():
    estudiantes_ref = db.collection("estudiantes").stream()
    estudiantes = []
    for doc in estudiantes_ref:
        estudiante = doc.to_dict()
        estudiante["id_estudiante"] = doc.id  # ID del documento en Firestore
        estudiantes.append(estudiante)

    return render_template('estudiantes/listar.html', estudiantes=estudiantes)

# CREATE -> CREAR ESTUDIANTE
@estudiante_bp.route('/estudiantes/crear', methods=['GET', 'POST'])
def crear_estudiante():
    if request.method == 'POST':
        data = {
            "nombre": request.form['nombre'],
            "apellido": request.form['apellido'],
            "documento": request.form['documento'],
            "id_programa": request.form['id_programa'],
            "semestre_actual": int(request.form['semestre_actual']),
            "estado": request.form['estado']
        }
        db.collection("estudiantes").add(data)
        return redirect('/estudiantes')

    return render_template('estudiantes/crear.html')

# UPDATE -> EDITAR ESTUDIANTE
@estudiante_bp.route('/estudiantes/editar/<id_estudiante>', methods=['GET', 'POST'])
@requiere_roles(['admin'])
def editar_estudiante(id_estudiante):
    estudiante_ref = db.collection("estudiantes").document(id_estudiante)

    if request.method == 'POST':
        data = {
            "nombre": request.form['nombre'],
            "apellido": request.form['apellido'],
            "documento": request.form['documento'],
            "id_programa": request.form['id_programa'],
            "semestre_actual": int(request.form['semestre_actual']),
            "estado": request.form['estado']
        }
        estudiante_ref.update(data)
        return redirect('/estudiantes')

    estudiante = estudiante_ref.get().to_dict()
    estudiante["id_estudiante"] = id_estudiante
    return render_template('estudiantes/editar.html', estudiante=estudiante)

# DELETE -> ELIMINAR ESTUDIANTE
@estudiante_bp.route('/estudiantes/eliminar/<id_estudiante>')
@requiere_roles(['admin'])
def eliminar_estudiante(id_estudiante):
    db.collection("estudiantes").document(id_estudiante).delete()
    return redirect('/estudiantes')
