from flask import Blueprint, render_template, redirect
from firebase_admin import firestore
from firebase_config import db

# Blueprint de alertas
alerta_bp = Blueprint('alerta', __name__)
db = firestore.client()

# READ -> LISTAR ALERTAS
@alerta_bp.route('/alertas')
def listar_alertas():
    alertas_ref = db.collection("alertas").order_by("fecha_generacion", direction=firestore.Query.DESCENDING)
    docs = alertas_ref.stream()

    alertas = []
    for doc in docs:
        alerta = doc.to_dict()
        alerta["id_alerta"] = doc.id

        # Buscar matrícula asociada
        if "id_matricula" in alerta:
            matricula_ref = db.collection("matriculas").document(alerta["id_matricula"]).get()
            if matricula_ref.exists:
                matricula = matricula_ref.to_dict()
                alerta["nota_final"] = matricula.get("nota_final")

                # Buscar estudiante asociado
                if "id_estudiante" in matricula:
                    estudiante_ref = db.collection("estudiantes").document(matricula["id_estudiante"]).get()
                    if estudiante_ref.exists:
                        estudiante = estudiante_ref.to_dict()
                        alerta["estudiante"] = estudiante.get("nombre")

        alertas.append(alerta)

    return render_template('alertas/listar.html', alertas=alertas)

# UPDATE -> CAMBIAR ESTADO DE ALERTA
@alerta_bp.route('/alertas/atender/<id_alerta>')
def atender_alerta(id_alerta):
    alerta_ref = db.collection("alertas").document(id_alerta)
    alerta_ref.update({"estado": "atendida"})
    return redirect('/alertas')

# DELETE -> ELIMINAR ALERTA
@alerta_bp.route('/alertas/eliminar/<id_alerta>')
def eliminar_alerta(id_alerta):
    alerta_ref = db.collection("alertas").document(id_alerta)
    alerta_ref.delete()
    return redirect('/alertas')
