from flask import current_app


def classify_intent(messaggio: str) -> str:
    """
    Classifica il messaggio in uno di tre intent:
    'prenotazione' | 'raccomandazione' | 'medica'
    """
    prompt = f"""Classifica il seguente messaggio di un paziente in UNA di queste categorie:
- prenotazione: vuole fissare, cancellare o modificare un appuntamento
- raccomandazione: descrive sintomi o problemi e vuole sapere quale medico consultare
- medica: domanda medica generica, informazioni su malattie, farmaci, procedure

Rispondi SOLO con una parola tra: prenotazione, raccomandazione, medica

Messaggio: {messaggio}
Categoria:"""

    llm = current_app.llm
    response = llm.invoke(prompt)
    result = getattr(response, "content", str(response)).strip().lower()

    if result not in ("prenotazione", "raccomandazione", "medica"):
        return "medica"  # fallback sicuro
    return result


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

    prompt = f"""Sei un assistente medico basato su evidenze.

Usa SOLO il contesto fornito per rispondere.
Se l'informazione non è presente nel contesto, rispondi: "Non ho informazioni sufficienti."

NON fare diagnosi definitive. NON prescrivere farmaci.
Se il caso è potenzialmente grave, suggerisci assistenza medica immediata.
{clinical_note}

Contesto:
{context}

Domanda:
{query}

Risposta:"""

    llm = current_app.llm
    response = llm.invoke(prompt)
    return getattr(response, "content", str(response))