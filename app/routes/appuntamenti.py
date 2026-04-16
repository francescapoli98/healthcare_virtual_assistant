from flask import Blueprint, request, jsonify
from ..models import Appuntamento #..models.appuntamenti se crei cartella \models
from ..core import db
from datetime import datetime, timedelta

appuntamenti_bp = Blueprint("appuntamenti", __name__)

#### gestione appuntamento con check per sovrapposizioni

@appuntamenti_bp.route("/appuntamenti", methods=["POST"])
def crea_appuntamento():
    data = request.json

    medico_id = data["medico_id"]
    paziente_id = data["paziente_id"]
    data_ora = datetime.strptime(data["data_ora"], "%Y-%m-%d %H:%M")
    #check conflitti
    existing = Appuntamento.query.filter_by(
        medico_id=medico_id,
        data_ora=data_ora
    ).first()

    if existing:
        return jsonify({"error": "Slot già occupato"}), 409

    app = Appuntamento(
        medico_id=medico_id,
        paziente_id=paziente_id,
        data_ora=data_ora,
        durata_minuti=data.get("durata_minuti", 30),
        note=data.get("note"),
        stato="programmato"
    )

    db.session.add(app)
    db.session.commit()

    return jsonify({"message": "Appuntamento creato", "id": app.id}), 201

#### vista appuntamenti di un paziente
@appuntamenti_bp.route("/pazienti/<int:paziente_id>/appuntamenti", methods=["GET"])
def get_appuntamenti_paziente(paziente_id):
    apps = Appuntamento.query.filter_by(paziente_id=paziente_id).all()

    result = []
    for a in apps:
        result.append({
            "id": a.id,
            "medico_id": a.medico_id,
            "data_ora": a.data_ora,
            "durata": a.durata_minuti,
            "stato": a.stato
        })

    return jsonify(result)

#### cancellazione appuntamento
@appuntamenti_bp.route("/appuntamenti/<int:id>", methods=["DELETE"])
def annulla_appuntamento(id):
    app = Appuntamento.query.get(id)

    if not app:
        return jsonify({"error": "Non trovato"}), 404

    app.stato = "annullato"
    db.session.commit()

    return jsonify({"message": "Appuntamento annullato"})


