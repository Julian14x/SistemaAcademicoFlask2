from flask import Blueprint, render_template, session, redirect
from firebase_admin import firestore
from routes.auth_routes import requiere_roles
from firebase_config import db


dashboard_bp = Blueprint('dashboard', __name__)
db = firestore.client()

@dashboard_bp.route('/dashboard')
@requiere_roles(['admin'])
def dashboard():
    if 'usuario' not in session:
        return redirect('/login')

    # Total estudiantes
    total_estudiantes = db.collection("estudiantes").get()
    total_estudiantes = len(total_estudiantes)

    # Alertas activas
    total_alertas = db.collection("alertas").where("estado", "==", "activa").get()
    total_alertas = len(total_alertas)

    # Riesgo alto: criterio basado en nota_final < 3.0 o asistencia < 70
    riesgo_alto = db.collection("matriculas") \
        .where("nota_final", "<", 3.0).get()
    riesgo_alto_count = len(riesgo_alto)

    riesgo_asistencia = db.collection("matriculas") \
        .where("asistencia", "<", 70).get()
    riesgo_alto_count += len(riesgo_asistencia)

    # Promedio general
    matriculas = db.collection("matriculas").get()
    notas = [m.to_dict().get("nota_final", 0) for m in matriculas if m.to_dict().get("nota_final") is not None]
    promedio_general = sum(notas) / len(notas) if notas else 0

    return render_template(
        'dashboard/reporte.html',
        total_estudiantes=total_estudiantes,
        total_alertas=total_alertas,
        riesgo_alto=riesgo_alto_count,
        promedio_general=promedio_general
    )
