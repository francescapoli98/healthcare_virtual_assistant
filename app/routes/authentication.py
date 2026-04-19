from flask import Blueprint, request, jsonify, session
from ..models import Paziente
from ..core import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    if Paziente.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email già registrata"}), 409

    p = Paziente(
        nome=data["nome"],
        cognome=data["cognome"],
        email=data["email"]
    )
    p.set_password(data["password"])
    db.session.add(p)
    db.session.commit()
    session["paziente_id"] = p.id
    return jsonify({"id": p.id, "nome": p.nome, "cognome": p.cognome}), 201

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    p = Paziente.query.filter_by(email=data["email"]).first()
    if not p or not p.check_password(data["password"]):
        return jsonify({"error": "Credenziali non valide"}), 401
    session["paziente_id"] = p.id
    return jsonify({"id": p.id, "nome": p.nome, "cognome": p.cognome})

@auth_bp.route("/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logout effettuato"})

@auth_bp.route("/auth/me", methods=["GET"])
def me():
    pid = session.get("paziente_id")
    if not pid:
        return jsonify({"error": "Non autenticato"}), 401
    p = Paziente.query.get(pid)
    if not p:
        return jsonify({"error": "Utente non trovato"}), 404
    return jsonify({"id": p.id, "nome": p.nome, "cognome": p.cognome})