from langchain_google_genai import ChatGoogleGenerativeAI

llm = None

def init_llm(app):
    global llm

    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=app.config["GOOGLE_API_KEY"],
        temperature=0.3
    )