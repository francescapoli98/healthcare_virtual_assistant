from flask import Blueprint, request, jsonify
from ..core import db
from ..models import ChatSessione, ChatMessaggio, Medico
from ..rag.retriever import retrieve_context
from ..rag.ai_client import handle_user_query #analyze_query, generate_response

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat/messaggio", methods=["POST"])
def invia_messaggio():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Messaggio mancante"}), 400

    messaggio = data["message"]
    paziente_id = data.get("paziente_id", 1)
    sessione_id = data.get("sessione_id")

    # 1. Gestione Sessione SQL (per persistenza a lungo termine)
    if not sessione_id:
        sessione = ChatSessione(paziente_id=paziente_id)
        db.session.add(sessione)
        db.session.commit()
        sessione_id = sessione.id

    # 2. CHIAMATA ALL'ORCHESTRATORE (L'AI che ora ha memoria)
    # Questa funzione ora gestisce internamente analyze, summarize, RAG e add_message
    ai_response = handle_user_query(messaggio, sessione_id)

    # 3. SINCRONIZZAZIONE DB (Opzionale, se vuoi tenere i messaggi anche su SQL)
    # Nota: handle_user_query salva già in SESSION_MEMORY (RAM)
    # Se vuoi salvarli anche nel DB fisico per lo storico:
    db.session.add(ChatMessaggio(sessione_id=sessione_id, ruolo="utente", contenuto=messaggio))
    db.session.add(ChatMessaggio(sessione_id=sessione_id, ruolo="assistente", contenuto=ai_response["content"]))
    db.session.commit()

    # 4. RISPOSTA AL FRONTEND
    response_data = {
        "sessione_id": sessione_id,
        "response": ai_response["content"],
        "action": ai_response.get("action"),
        "analysis": ai_response.get("analysis")
    }
    
    return jsonify(response_data)



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


def gestisci_richiesta(messaggio):
    # Una sola chiamata LLM per intent + triage + sintomi
    analysis = analyze_query(messaggio)

    intent   = analysis.get("intent", "medica")
    triage   = analysis.get("triage", "normale")
    severity = analysis.get("severity", "media")
    specialty = analysis.get("specialty", "")

    # Gestione urgenze — bypassa il RAG e risponde subito
    if triage == "urgente":
        risposta = (
            "⚠️ I sintomi che descrivi potrebbero essere gravi. "
            "Ti consiglio di chiamare il 118 o recarti al pronto soccorso immediatamente. "
            "Non attendere un appuntamento ordinario."
        )
        return risposta, {"intent": "urgente", "triage": "urgente", "severity": severity}

    if intent == "prenotazione":
        testo = (
            "Certo! Puoi usare il form di prenotazione qui a lato, "
            "oppure dimmi il nome del medico e la data che preferisci."
        )
        return testo, {"intent": "prenotazione", "triage": triage}

    if intent == "raccomandazione":
        return gestisci_raccomandazione(messaggio, specialty, triage)

    # intent == "medica"
    context = retrieve_context(messaggio)
    risposta = generate_response(messaggio, context)

    # Aggiunge avviso triage se severità media/alta
    if triage == "attenzione":
        risposta += "\n\n⚠️ I sintomi che descrivi meritano attenzione. Ti consiglio di consultare un medico presto."

    return risposta, {"intent": "medica", "triage": triage, "severity": severity}


def gestisci_raccomandazione(messaggio, specialty, triage):
    context = retrieve_context(messaggio)
    risposta_rag = generate_response(messaggio, context)

    medici = []
    if specialty:
        risultati = Medico.query.filter(
            Medico.specializzazione.ilike(f"%{specialty}%")
        ).all()
        medici = [
            {"id": m.id, "nome": f"{m.nome} {m.cognome}",
             "specializzazione": m.specializzazione}
            for m in risultati
        ]

    testo = risposta_rag
    if medici:
        nomi = ", ".join(m["nome"] for m in medici)
        testo += f"\n\nPer questa problematica ti consiglio: {nomi}. Vuoi prenotare?"

    return testo, {"intent": "raccomandazione", "triage": triage, "medici": medici}




        ##### old version
# @chat_bp.route("/chat/messaggio", methods=["POST"])
# def invia_messaggio():
#     data = request.get_json()
#     if not data or "message" not in data:
#         return jsonify({"error": "Messaggio mancante"}), 400

#     messaggio = data["message"]
#     paziente_id = data.get("paziente_id", 1)

#     sessione_id = data.get("sessione_id")
#     if not sessione_id:
#         sessione = ChatSessione(paziente_id=paziente_id)
#         db.session.add(sessione)
#         db.session.commit()
#         sessione_id = sessione.id

#     db.session.add(ChatMessaggio(
#         sessione_id=sessione_id,
#         ruolo="utente",
#         contenuto=messaggio
#     ))
#     db.session.commit()

#     risposta, extra = gestisci_richiesta(messaggio)

#     db.session.add(ChatMessaggio(
#         sessione_id=sessione_id,
#         ruolo="assistente",
#         contenuto=risposta
#     ))
#     db.session.commit()

#     response = {"sessione_id": sessione_id, "response": risposta}
#     if extra:
#         response.update(extra)

#     return jsonify(response)