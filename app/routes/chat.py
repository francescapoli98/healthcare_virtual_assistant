from flask import Blueprint, request, jsonify, current_app
from ..core import db
from ..models import ChatSessione, ChatMessaggio, Medico, Appuntamento
from ..rag.retriever import retrieve_context
from ..rag.ai_client import generate_response, classify_intent

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat/messaggio", methods=["POST"])
def invia_messaggio():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Messaggio mancante"}), 400

    messaggio = data["message"]
    paziente_id = data.get("paziente_id", 1)

    # Recupera o crea sessione
    sessione_id = data.get("sessione_id")
    if not sessione_id:
        sessione = ChatSessione(paziente_id=paziente_id)
        db.session.add(sessione)
        db.session.commit()
        sessione_id = sessione.id

    # Salva messaggio utente
    db.session.add(ChatMessaggio(
        sessione_id=sessione_id,
        ruolo="utente",
        contenuto=messaggio
    ))
    db.session.commit()

    # Gestisci la richiesta
    risposta, extra = gestisci_richiesta(messaggio)

    # Salva risposta assistente
    db.session.add(ChatMessaggio(
        sessione_id=sessione_id,
        ruolo="assistente",
        contenuto=risposta
    ))
    db.session.commit()

    response = {
        "sessione_id": sessione_id,
        "response": risposta
    }
    if extra:
        response.update(extra)  # es. {"intent": "prenotazione", "medici": [...]}

    return jsonify(response)


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
    """
    Ritorna (risposta_testuale, extra_dict).
    extra_dict può contenere intent e dati strutturati per il frontend.
    """
    intent = classify_intent(messaggio)

    if intent == "prenotazione":
        return gestisci_prenotazione(messaggio)

    elif intent == "raccomandazione":
        return gestisci_raccomandazione(messaggio)

    else:  # intent == "medica" o fallback
        context = retrieve_context(messaggio)
        risposta = generate_response(messaggio, context)
        return risposta, {"intent": "medica"}


def gestisci_raccomandazione(messaggio):
    """
    Il RAG capisce il problema, suggerisce la specializzazione,
    poi recupera i medici disponibili dal DB.
    """
    context = retrieve_context(messaggio)
    risposta_rag = generate_response(messaggio, context)

    # Estrai la specializzazione suggerita dall'LLM
    specializzazione = extract_specializzazione(messaggio)
    medici = []

    if specializzazione:
        risultati = Medico.query.filter(
            Medico.specializzazione.ilike(f"%{specializzazione}%")
        ).all()
        medici = [
            {"id": m.id, "nome": f"{m.nome} {m.cognome}",
             "specializzazione": m.specializzazione}
            for m in risultati
        ]

    testo = risposta_rag
    if medici:
        nomi = ", ".join(m["nome"] for m in medici)
        testo += f"\n\nPer questa problematica ti consiglio di consultare: {nomi}."
        testo += " Vuoi prenotare un appuntamento?"

    return testo, {"intent": "raccomandazione", "medici": medici}


def gestisci_prenotazione(messaggio):
    testo = (
        "Certo! Puoi usare il form di prenotazione qui a lato, "
        "oppure dimmi il nome del medico e la data che preferisci."
    )
    return testo, {"intent": "prenotazione"}


def extract_specializzazione(messaggio):
    """
    Chiede all'LLM di estrarre la specializzazione medica più adatta.
    Ritorna una stringa come 'Cardiologia' o None.
    """
    from flask import current_app
    prompt = f"""Dato il seguente messaggio di un paziente, rispondi SOLO con la specializzazione
medica più appropriata (es: Cardiologia, Dermatologia, Pneumologia, Ortopedia, ecc.).
Se non è chiaro, rispondi con: nessuna.

Messaggio: {messaggio}
Specializzazione:"""

    llm = current_app.llm
    response = llm.invoke(prompt)
    result = getattr(response, "content", str(response)).strip()
    return None if result.lower() == "nessuna" else result