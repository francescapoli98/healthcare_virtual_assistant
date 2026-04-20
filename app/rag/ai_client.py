from flask import current_app

def analyze_query(messaggio: str) -> dict:
    prompt = f"""
Analizza il messaggio di un paziente ed estrai queste informazioni in formato JSON:

- intent: "prenotazione", "raccomandazione", "medica"
- symptoms: lista di sintomi (se presenti)
- severity: "bassa", "media", "alta"
- specialty: specializzazione medica più rilevante (es. cardiologia, dermatologia, ecc.)
- triage: "normale", "attenzione", "urgente"

Regole:
- "urgente" se sintomi potenzialmente gravi (es. dolore al petto, difficoltà respiratoria)
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


def generate_response(query: str, context_data: dict | str) -> str:
    if isinstance(context_data, dict):
        context = context_data["context"]
        has_clinical = context_data.get("has_clinical_cases", False)
    else:
        context = context_data
        has_clinical = False

    clinical_note = (
        "Il contesto include casi clinici sintetici da dataset medici certificati. "
        "Usali per confrontare pattern clinici, senza riferimenti a pazienti specifici."
        if has_clinical else ""
    )

    prompt = f"""Sei un assistente medico basato su evidenze. Il tuo ruolo è informare e supportare, non sostituire il medico.

Istruzioni:
- Usa SOLO il contesto fornito
- Cita SEMPRE le fonti usando [Fonte X]
- Se l'informazione non è nel contesto, dì: "Non ho informazioni sufficienti su questo argomento."
- NON fare diagnosi definitive. NON prescrivere farmaci specifici.
- Se il caso è potenzialmente grave o urgente, suggerisci di cercare assistenza medica immediata.
- Alla fine di ogni risposta, aggiungi SEMPRE una frase che ricorda di consultare un medico e chiedi se il paziente vuole prenotare una visita.
{clinical_note}

Contesto:
{context}

Domanda del paziente:
{query}

Risposta (concludi sempre chiedendo se vuole prenotare una visita):"""

    llm = current_app.llm
    response = llm.invoke(prompt)
    return getattr(response, "content", str(response))


### prima di triage, avevo una classificazione dei casi d'uso del chatbot in base ai messaggi dell'utente

      
# def classify_intent(messaggio: str) -> str:
#     prompt = f"""Classifica il seguente messaggio di un paziente in UNA di queste categorie:

# - prenotazione: vuole ESPLICITAMENTE fissare, cancellare o modificare un appuntamento. Esempi: "voglio prenotare", "fissa un appuntamento", "cancella la visita".
# - raccomandazione: chiede ESPLICITAMENTE quale medico consultare o quale specialista vedere. Esempi: "quale medico devo vedere?", "chi devo contattare per...?", "mi consigli uno specialista".
# - medica: descrive sintomi, chiede informazioni su malattie, farmaci, cure, o cosa fare per un problema di salute. Esempi: "ho la tosse", "mi fa male la testa", "cosa posso fare per...", "ho la febbre".

# IMPORTANTE: se il paziente descrive sintomi o chiede cosa fare per un disturbo, classifica SEMPRE come "medica", anche se potrebbe avere bisogno di un medico.

# Rispondi SOLO con una parola tra: prenotazione, raccomandazione, medica

# Messaggio: {messaggio}
# Categoria:"""

#     llm = current_app.llm
#     response = llm.invoke(prompt)
#     result = getattr(response, "content", str(response)).strip().lower()

#     if result not in ("prenotazione", "raccomandazione", "medica"):
#         return "medica"
#     return result