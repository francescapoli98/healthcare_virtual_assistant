from langchain_google_genai import ChatGoogleGenerativeAI #used all tokens
from langchain_groq import ChatGroq

###### GOOGLE AI(gemini)
# def create_llm(app):
#     return ChatGoogleGenerativeAI(
#         model="gemini-2.0-flash", 
#         google_api_key=app.config["GOOGLE_API_KEY"],
#         temperature=0.3
#     )

###### GROQ (llama)
def create_llm(app):
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=app.config["GROQ_API_KEY"],
        temperature=0.3
    )

llm_instance = None

def get_llm(app):
    global llm_instance

    if llm_instance is None:
        llm_instance = create_llm(app)

    return llm_instance