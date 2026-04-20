import os

class Config:
    SECRET_KEY = "la-tua-chiave-generata"
    ## mysql db
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/gestione_appuntamenti"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ## gemini AI API
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyAl8iiIqOD0ndpjWpqGR69huZuWY1vHVYs")
    ## huggingface
    HF_TOKEN = os.getenv("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")
    ## groq
    GROQ_API_KEY="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"