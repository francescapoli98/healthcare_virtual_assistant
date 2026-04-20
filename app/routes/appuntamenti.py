from flask import Blueprint, request, jsonify
from ..models import Appuntamento, Medico #..models.appuntamenti se crei cartella \models
from ..core import db
from datetime import datetime, timedelta
from sqlalchemy import func

appuntamenti_bp = Blueprint("appuntamenti", __name__)

#### gestione appuntamento con check per sovrapposizioni

@appuntamenti_bp.route("", methods=["POST"])
def crea_appuntamento():
    data = request.json

    medico_id = data["medico_id"]
    paziente_id = data["paziente_id"]
    durata = data.get("durata_minuti", 30)
    data_ora = datetime.strptime(data["data_ora"], "%Y-%m-%d %H:%M")

    if is_slot_busy(medico_id, data_ora, data.get("durata_minuti", 30)):
        return jsonify({"error": "Slot già occupato"}), 409

    app = Appuntamento(
        medico_id=medico_id,
        paziente_id=paziente_id,
        data_ora=data_ora,
        durata_minuti=durata,
        note=data.get("note"),
        stato="programmato"
    )

    db.session.add(app)
    db.session.commit()

    return jsonify({
        "message": "Appuntamento creato",
        "id": app.id
    }), 201


def is_slot_busy(medico_id, start_time, durata_richiesta):
    end_time = start_time + timedelta(minutes=durata_richiesta)
    
    # Cerchiamo se esiste un appuntamento che inizia ESATTAMENTE in quel momento
    # (Sfruttando il tuo UNIQUE INDEX a livello DB)
    existing = Appuntamento.query.filter_by(
        medico_id=medico_id, 
        data_ora=start_time
    ).first()
    
    return existing is not None

#### vista appuntamenti di un paziente
# @appuntamenti_bp.route("/pazienti/<int:paziente_id>/appuntamenti", methods=["GET"])
@appuntamenti_bp.route("/paziente/<int:paziente_id>", methods=["GET"])
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
@appuntamenti_bp.route("/<int:id>", methods=["DELETE"])
def annulla_appuntamento(id):
    app = Appuntamento.query.get(id)

    if not app:
        return jsonify({"error": "Non trovato"}), 404

    app.stato = "annullato"
    db.session.commit()

    return jsonify({"message": "Appuntamento annullato"})

from ..models import Medico  # aggiungi questo all'import esistente

@appuntamenti_bp.route("/medici", methods=["GET"])
def get_medici():
    medici = Medico.query.all()
    return jsonify([
        {
            "id": m.id,
            "nome": f"{m.nome} {m.cognome}",
            "specializzazione": m.specializzazione
        }
        for m in medici
    ])

@appuntamenti_bp.route("/medici/<int:medico_id>/slot-occupati", methods=["GET"])
def get_slot_occupati(medico_id):
    from_date = request.args.get("from")  # es. "2026-04-01"
    to_date = request.args.get("to")      # es. "2026-04-30"

    query = Appuntamento.query.filter(
        Appuntamento.medico_id == medico_id,
        Appuntamento.stato != "annullato"
    )

    if from_date:
        query = query.filter(Appuntamento.data_ora >= datetime.strptime(from_date, "%Y-%m-%d"))
    if to_date:
        to_dt = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1)
        query = query.filter(Appuntamento.data_ora < to_dt)

    apps = query.all()
    return jsonify([
        a.data_ora.strftime("%Y-%m-%d %H:%M") for a in apps
    ])

@appuntamenti_bp.route("/medici/<int:medico_id>/slot-disponibili", methods=["GET"])
def get_slot_disponibili(medico_id):
    date = request.args.get("date")  # YYYY-MM-DD

    occupied = get_slot_occupati(medico_id).json

    all_slots = []
    start = datetime.strptime(date + " 09:00", "%Y-%m-%d %H:%M")
    end   = datetime.strptime(date + " 18:00", "%Y-%m-%d %H:%M")

    while start < end:
        slot = start.strftime("%Y-%m-%d %H:%M")

        if slot not in occupied:
            all_slots.append(slot)

        start += timedelta(minutes=30)

    return jsonify(all_slots)

