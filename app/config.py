import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-dev-key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "mysql+pymysql://root:@localhost/gestione_appuntamenti"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GROQ_API_KEY   = os.getenv("GROQ_API_KEY")
    HF_TOKEN       = os.getenv("HF_TOKEN")