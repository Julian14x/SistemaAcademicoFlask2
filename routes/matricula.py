from flask import Blueprint, render_template, request, redirect, session
from firebase_admin import firestore
from routes.auth_routes import requiere_roles
from firebase_config import db

matricula_bp = Blueprint('matricula', __name__)
db = firestore.client()


# LISTAR MATRÍCULAS
@matricula_bp.route('/matriculas')
@requiere_roles(['admin'])
def listar_matriculas():
    if 'usuario' not in session:
        return redirect('/login')

    docs = db.collection("matriculas").stream()
    matriculas = []
    for doc in docs:
        m = doc.to_dict()
        m["id_matricula"] = doc.id

        # Buscar nombre del estudiante
        if "id_estudiante" in m:
            estudiante_ref = db.collection("estudiantes").document(m["id_estudiante"]).get()
            if estudiante_ref.exists:
                estudiante = estudiante_ref.to_dict()
                m["estudiante_nombre"] = estudiante.get("nombre")

        # Buscar nombre de la asignatura
        if "id_asignatura" in m:
            asignatura_ref = db.collection("asignaturas").document(m["id_asignatura"]).get()
            if asignatura_ref.exists:
                asignatura = asignatura_ref.to_dict()
                m["asignatura_nombre"] = asignatura.get("nombre")

        matriculas.append(m)

    return render_template('matriculas/listar.html', matriculas=matriculas)


# CREAR MATRÍCULA
@matricula_bp.route('/matriculas/crear', methods=['GET', 'POST'])
def crear_matricula():
    if 'usuario' not in session:
        return redirect('/login')

    estudiantes = [e.to_dict() | {"id_estudiante": e.id} for e in db.collection("estudiantes").stream()]
    asignaturas = [a.to_dict() | {"id_asignatura": a.id} for a in db.collection("asignaturas").stream()]

    if request.method == 'POST':
        id_estudiante = request.form['id_estudiante']
        id_asignatura = request.form['id_asignatura']
        periodo_academico = request.form['periodo_academico']
        nota_final = float(request.form['nota_final'])
        porcentaje_asistencia = float(request.form['porcentaje_asistencia'])

        # Insertar matrícula
        matricula_ref = db.collection("matriculas").add({
            "id_estudiante": id_estudiante,
            "id_asignatura": id_asignatura,
            "periodo_academico": periodo_academico,
            "nota_final": nota_final,
            "porcentaje_asistencia": porcentaje_asistencia
        })

        # Generar alerta si aplica
        if nota_final < 3.0 or porcentaje_asistencia < 70:
            nivel_riesgo = "Alto"
        elif nota_final < 3.5 or porcentaje_asistencia < 80:
            nivel_riesgo = "Medio"
        else:
            nivel_riesgo = "Bajo"

        if nivel_riesgo in ("Alto", "Medio"):
            db.collection("alertas").add({
                "id_matricula": matricula_ref[1].id,
                "estudiante": id_estudiante,
                "nivel_riesgo": nivel_riesgo,
                "fecha_generacion": firestore.SERVER_TIMESTAMP,
                "estado": "activa"
            })

        return redirect('/matriculas')

    return render_template('matriculas/crear.html', estudiantes=estudiantes, asignaturas=asignaturas)

# EDITAR MATRÍCULA
@matricula_bp.route('/matriculas/editar/<id_matricula>', methods=['GET', 'POST'])
def editar_matricula(id_matricula):
    if 'usuario' not in session:
        return redirect('/login')

    matricula_ref = db.collection("matriculas").document(id_matricula)

    if request.method == 'POST':
        data = {
            "periodo_academico": request.form['periodo_academico'],
            "nota_final": float(request.form['nota_final']),
            "porcentaje_asistencia": float(request.form['porcentaje_asistencia'])
        }
        matricula_ref.update(data)
        return redirect('/matriculas')

    matricula = matricula_ref.get().to_dict()
    matricula["id_matricula"] = id_matricula
    return render_template('matriculas/editar.html', matricula=matricula)

# ELIMINAR MATRÍCULA
@matricula_bp.route('/matriculas/eliminar/<id_matricula>')
def eliminar_matricula(id_matricula):
    if 'usuario' not in session:
        return redirect('/login')

    db.collection("matriculas").document(id_matricula).delete()
    return redirect('/matriculas')
