from flask import current_app
from app.rag.retriever import retrieve_context, semantic_check
from app.rag.memory import get_recent_context, add_message

# -----------------------------
# MEMORY (CONVERSATION SUMMARY)
# -----------------------------
def summarize_chat(history):
    if not history:
        return ""

    text = "\n".join([
        f"{m.get('role')}: {m.get('content', '')}"
        for m in history[-12:]])

    prompt = f"""
Riassumi la conversazione medico-paziente evidenziando SOLO informazioni clinicamente rilevanti.

{text}

Riassunto:
"""

    llm = current_app.llm
    response = llm.invoke(prompt)

    return getattr(response, "content", str(response))


# def build_context(chat_history, rag_context):
#     return {
#         "memory": summarize_chat(chat_history),
#         "rag": rag_context
#     }


# -----------------------------
# ANALISI QUERY (LLM)
# -----------------------------
def analyze_query(messaggio: str) -> dict:
    prompt = f"""
Analizza il messaggio di un paziente ed estrai queste informazioni in formato JSON:

- intent: "prenotazione", "raccomandazione", "medica"
- symptoms: lista di sintomi (se presenti)
- severity: "bassa", "media", "alta"
- specialty: specializzazione medica più rilevante
- triage: "normale", "attenzione", "urgente"

Regole:
- "urgente" se sintomi potenzialmente gravi
- NON inventare sintomi
- Rispondi SOLO JSON valido

Messaggio: {messaggio}
JSON:
"""

    llm = current_app.llm
    response = llm.invoke(prompt)
    content = getattr(response, "content", str(response))

    try:
        import json
        return json.loads(content)
    except:
        return {
            "intent": "medica",
            "symptoms": [],
            "severity": "media",
            "specialty": "medicina generale",
            "triage": "normale"
        }


# -----------------------------
# GENERAZIONE RISPOSTA (LLM)
# -----------------------------
def generate_response(query: str, context_data: dict, memory: str = "") -> str:
    context = context_data.get("context", "")
    confidence = context_data.get("confidence", 0.0)
    has_clinical = context_data.get("has_clinical_cases", False)

    # memory = summarize_chat(chat_history or [])

    clinical_note = (
        "Il contesto include casi clinici sintetici da dataset medici certificati."
        if has_clinical else ""
    )

    prompt = f"""
Sei un assistente sanitario.

MEMORIA CONVERSAZIONE:
{memory}

OBIETTIVO:
- Comprendere i sintomi dell’utente
- Collegare il messaggio alla memoria precedente
- Fornire informazioni basate su contesto e storia

REGOLE:
1. Rispondi SOLO se la domanda è medica
2. Se non hai informazioni: "Non ho informazioni sufficienti su questo argomento."
3. NON fare diagnosi definitive
4. NON prescrivere farmaci

COMPORTAMENTO:
- Usa memoria + contesto insieme (NON separatamente)
- Se i sintomi sono già stati menzionati, collegali
- Se confuso → chiedi chiarimenti
- NON chiedere sempre prenotazione

FLUSSO:
- interpreta sintomi
- fai 1 domanda di approfondimento
- SOLO DOPO suggerisci visita

Confidence contesto: {confidence}

{clinical_note}

Contesto RAG:
{context}

CONVERSAZIONE PRECEDENTE (riassunto operativo):
{memory}

Domanda:
{query}

Risposta:
"""

    llm = current_app.llm
    response = llm.invoke(prompt)
    return getattr(response, "content", str(response))


# -----------------------------
# ORCHESTRAZIONE COMPLETA
# -----------------------------
def handle_user_query(query: str, session_id: int):
    print(f"DEBUG: Session ID ricevuto: {session_id}")
    # 1. FILTRO SEMANTICO (Pre-analisi)
    sem, conf = semantic_check(query)

    # if sem == "non_medical":
    #     return {
    #         "content": "Non sono programmato per rispondere a questa domanda.",
    #         "action": None
    #     }

    # if sem == "uncertain":
    #     return {
    #         "content": "Non ho capito bene la tua richiesta. Puoi spiegarti meglio?",
    #         "action": None
    #     }

    # 2. AGGIORNAMENTO IMMEDIATO MEMORIA (Messaggio Utente)
    # Fondamentale: salviamo il messaggio PRIMA di generare il riassunto
    add_message(session_id, "user", query)

    # 3. RECUPERO STORIA E RAG
    # Ora chat_history contiene anche l'ultimo messaggio appena salvato
    chat_history = get_recent_context(session_id)
    memory_summary = summarize_chat(chat_history)
    
    context_data = retrieve_context(query)
    analysis = analyze_query(query)

    # 4. TRIAGE URGENTE
    if analysis.get("triage") == "urgente":
        response_text = (
            "I sintomi descritti potrebbero essere seri. "
            "Ti consiglio di contattare immediatamente un medico o il pronto soccorso."
        )
        add_message(session_id, "assistant", response_text)
        return {
            "content": response_text,
            "action": None,
            "analysis": analysis,
            "confidence": conf
        }

    # 5. GENERAZIONE RISPOSTA LLM
    # Passiamo il memory_summary generato con la storia aggiornata
    response = generate_response(query, context_data, memory_summary)

    # 6. LOGICA DI BUSINESS (Prenotazioni / Intent)
    action = None
    intent = analysis.get("intent")

    # Aggiunta suggerimento proattivo
    if intent in ["prenotazione", "raccomandazione"]:
        if "si" not in query.lower(): # Evita di ripeterlo se l'utente ha già detto sì
            response += "\n\nVuoi che ti aiuti a trovare lo specialista più adatto?"

    # Trigger booking UI
    if intent == "prenotazione" and "si" in query.lower():
        action = "open_booking"
        response = "Perfetto, procediamo con la prenotazione."

    # 7. AGGIORNAMENTO MEMORIA (Risposta Assistente)
    add_message(session_id, "assistant", response)

    return {
        "content": response,
        "action": action,
        "analysis": analysis,
        "confidence": conf
    }