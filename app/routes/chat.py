from flask import Blueprint, request, jsonify
### per gestione appuntamenti (funzione'basic' con query su mysql db)
from ..models import ChatSessione, ChatMessaggio
from ..core import db
### per consigli medici in chat (RAG + context + response generation)
# from rag.retriever import retrieve_context
# from rag.ai_client import generate_response

chat_bp = Blueprint("chat", __name__)
@chat_bp.route("/chat/sessione", methods=["POST"])
def crea_sessione():
    data = request.json

    sessione = ChatSessione(
        paziente_id=data["paziente_id"]
    )

    db.session.add(sessione)
    db.session.commit()

    return jsonify({"sessione_id": sessione.id})

#### gestione messaggi con RAG
@chat_bp.route("/chat/messaggio", methods=["POST"])
def invia_messaggio():
    data = request.json

    sessione_id = data["sessione_id"]
    testo = data["messaggio"]

    # salva messaggio utente
    msg_user = ChatMessaggio(
        sessione_id=sessione_id,
        ruolo="utente",
        contenuto=testo
    )
    db.session.add(msg_user)

    # RAG
    context = retrieve_context(testo)
    risposta = generate_response(testo, context)

    # salva risposta AI
    msg_ai = ChatMessaggio(
        sessione_id=sessione_id,
        ruolo="assistente",
        contenuto=risposta
    )
    db.session.add(msg_ai)

    db.session.commit()

    return jsonify({"risposta": risposta})

@chat_bp.route("/chat/sessione/<int:sessione_id>", methods=["GET"])
def get_chat(sessione_id):
    messaggi = ChatMessaggio.query.filter_by(
        sessione_id=sessione_id
    ).order_by(ChatMessaggio.creato_il).all()

    result = [
        {
            "ruolo": m.ruolo,
            "contenuto": m.contenuto,
            "timestamp": m.creato_il
        }
        for m in messaggi
    ]

    return jsonify(result)