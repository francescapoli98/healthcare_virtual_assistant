from ..extensions import llm

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

    response = llm.invoke(prompt)
    return response.content