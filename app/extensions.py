from langchain_google_genai import ChatGoogleGenerativeAI

def create_llm(app):
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=app.config["GOOGLE_API_KEY"],
        temperature=0.3
    )

# llm = init_llm(app)