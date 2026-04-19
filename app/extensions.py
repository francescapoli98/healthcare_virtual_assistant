from langchain_google_genai import ChatGoogleGenerativeAI

def create_llm(app):
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=app.config["GOOGLE_API_KEY"],
        temperature=0.3
    )

llm_instance = None

def get_llm(app):
    global llm_instance

    if llm_instance is None:
        llm_instance = create_llm(app)

    return llm_instance