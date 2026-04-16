from flask import Blueprint, request
from ..core import db
from ..models import ChatSessione, ChatMessaggio
### per consigli medici in chat (RAG + context + response generation)
# from rag.retriever import retrieve_context
# from rag.ai_client import generate_response

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat/messaggio", methods=["POST"])
def invia_messaggio():
    data = request.json
    messaggio = data.get("messaggio")
    sessione_id = data.get("sessione_id")

    # crea sessione se non esiste
    if not sessione_id:
        sessione = ChatSessione(paziente_id=1)  # per ora fisso
        db.session.add(sessione)
        db.session.commit()
        sessione_id = sessione.id

    # salva messaggio utente
    user_msg = ChatMessaggio(
        sessione_id=sessione_id,
        ruolo="utente",
        contenuto=messaggio
    )
    db.session.add(user_msg)

    # risposta agente (placeholder AI)
    risposta_test = f"Ho ricevuto: {messaggio}"

    # salva risposta assistente
    bot_msg = ChatMessaggio(
        sessione_id=sessione_id,
        ruolo="assistente",
        contenuto=risposta_test
    )
    db.session.add(bot_msg)

    db.session.commit()

    return {
        "sessione_id": sessione_id,
        "risposta": risposta_test
    }