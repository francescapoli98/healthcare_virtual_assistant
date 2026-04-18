from flask import current_app

def generate_response(query, context):
    prompt = f"""
    Sei un assistente medico.

    Contesto:
    {context}

    Domanda:
    {query}

    Rispondi in modo chiaro.
    NON fare diagnosi definitive.
    Suggerisci di consultare un medico.
    """

    llm = current_app.llm  # ✅ prende l'LLM dall'app

    response = llm.invoke(prompt)
    return getattr(response, "content", str(response))