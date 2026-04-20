from flask import Blueprint, request, jsonify
from ..core import db
from ..models import ChatSessione, ChatMessaggio, Medico
from ..rag.ai_client import handle_user_query

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat/messaggio", methods=["POST"])
def invia_messaggio():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Messaggio mancante"}), 400

    messaggio = data["message"]
    paziente_id = data.get("paziente_id", 1)
    sessione_id = data.get("sessione_id")

    # Sessione SQL
    if not sessione_id:
        sessione = ChatSessione(paziente_id=paziente_id)
        db.session.add(sessione)
        db.session.commit()
        sessione_id = sessione.id

    # Chiamata pipeline (AI con memoria)
    ai_response = handle_user_query(messaggio, sessione_id)
    
    # Estraiamo l'analisi fatta dall'AI per decidere cosa fare
    analysis = ai_response.get("analysis", {})    
    intent = analysis.get("intent", "medica")
    specialty = analysis.get("specialty", "")
    risposta_testuale = ai_response["content"]
    
    medici_list = []

    # EXTRA: Ricerca Medici
    if intent == "raccomandazione" and specialty:
        risultati = Medico.query.filter(
            Medico.specializzazione.ilike(f"%{specialty}%")
        ).all()
        medici_list = [
            {
                "id": m.id, 
                "nome": f"{m.nome} {m.cognome}",
                "specializzazione": m.specializzazione
            } for m in risultati
        ]
        
        if medici_list:
            nomi = ", ".join([m["nome"] for m in medici_list])
            if "ti consiglio" not in risposta_testuale.lower():
                risposta_testuale += f"\n\nPer questa problematica ti consiglio: {nomi}. Vuoi prenotare?"

    # SINCRONIZZAZIONE DB FISICO
    db.session.add(ChatMessaggio(sessione_id=sessione_id, ruolo="utente", contenuto=messaggio))
    db.session.add(ChatMessaggio(sessione_id=sessione_id, ruolo="assistente", contenuto=risposta_testuale))
    db.session.commit()

    # RISPOSTA AL FRONTEND 
    return jsonify({
        "sessione_id": sessione_id,
        "response": risposta_testuale,
        "intent": intent,
        "triage": analysis.get("triage"),
        "medici": medici_list,
        "action": ai_response.get("action")
    })

@chat_bp.route("/chat/sessione/<int:paziente_id>", methods=["GET"])
def get_storico(paziente_id):
    sessione = ChatSessione.query.filter_by(
        paziente_id=paziente_id
    ).order_by(ChatSessione.id.desc()).first()

    if not sessione:
        return jsonify([])

    messaggi = ChatMessaggio.query.filter_by(
        sessione_id=sessione.id
    ).order_by(ChatMessaggio.id.asc()).all()

    return jsonify([
        {"ruolo": m.ruolo, "contenuto": m.contenuto}
        for m in messaggi
    ])